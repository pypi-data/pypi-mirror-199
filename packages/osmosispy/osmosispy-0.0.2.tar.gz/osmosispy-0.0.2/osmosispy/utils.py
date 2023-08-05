from osmosispy.exceptions import QueryError
from osmosis_proto.proto.tendermint.types.block_pb2 import Block
from osmosis_proto.proto.cosmos.tx.v1beta1.tx_pb2 import Tx
from osmosis_proto.proto.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from grpc import Channel
from google.protobuf import json_format, message
import grpc._channel
import grpc
from typing import Dict, List, Optional, Union
import collections
import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Union
from google.protobuf.timestamp_pb2 import Timestamp

# number of decimal places
PRECISION = 18


# reimplementation of cosmos-sdk/types/decimal.go
def to_sdk_dec(dec: float) -> str:
    '''
    create a decimal from an input decimal.
    valid must come in the form:
        (-) whole integers (.) decimal integers
    examples of acceptable input include:
        -123.456
        456.7890
        345
        -456789

    NOTE - An error will return if more decimal places
    are provided in the string than the constant Precision.

    CONTRACT - This function does not mutate the input str.
    '''
    dec_str = str(dec)

    if len(dec_str) == 0:
        raise TypeError(f'Expected decimal string but got: {dec_str}')

    # first extract any negative symbol
    neg = False
    if dec_str[0] == '-':
        neg = True
        dec_str = dec_str[1:]

    if len(dec_str) == 0:
        raise TypeError(f'Expected decimal string but got: {dec_str}')

    strs = dec_str.split('.')
    len_decs = 0
    combined_str = strs[0]

    if len(strs) == 2:  # has a decimal place
        len_decs = len(strs[1])
        if len_decs == 0 or len(combined_str) == 0:
            raise TypeError(f'Expected decimal string but got: {dec_str}')
        combined_str += strs[1]
    elif len(strs) > 2:
        raise TypeError(f'Expected decimal string but got: {dec_str}')

    if len_decs > PRECISION:
        raise TypeError(
            f'value \'{dec_str}\' exceeds max precision by {PRECISION-len_decs} decimal places: max precision {PRECISION}'
        )

    # add some extra zero's to correct to the Precision factor
    zeros_to_add = PRECISION - len_decs
    zeros = '0' * zeros_to_add
    combined_str += zeros

    try:
        int(combined_str, 10)
    except ValueError as err:
        raise ValueError(
            f'failed to set decimal string with base 10: {combined_str}'
        ) from err

    if neg:
        return '-' + combined_str

    return combined_str


def from_sdk_dec_24(dec_str: str) -> float:
    return float(dec_str) * 1e-24


def from_sdk_dec_n(dec_str: str, n: int = 6) -> float:
    return float(dec_str) * 10 ** (-n)


def format_fields_nested(
    object: Union[list, dict], fn: Callable[[Any], Any], fields: List[str]
) -> Union[list, dict]:
    """
    Format the fields inside a nested dictionary with the function provided

    Args:
        object (Union[list, dict]): The object to format
        fn (Callable[[Any], Any]): The function to format objects with
        fields (list[str]): The fields to format

    Returns:
        Union[list, dict]: The output formatted
    """
    if type(object) == dict:
        output = {}
        for k, v in object.items():
            if type(v) in (dict, list):
                output[k] = format_fields_nested(v, fn, fields)
            else:
                if k in fields:
                    output[k] = fn(v)
                else:
                    output[k] = v

        return output

    if type(object) == list:
        output = []

        for element in object:
            if type(object) in (dict, list):
                output.append(format_fields_nested(element, fn, fields))
            else:
                output.append(element)

        return output


def from_sdk_dec(dec_str: str) -> float:
    if dec_str is None or dec_str == '':
        return 0

    if '.' in dec_str:
        raise TypeError(
            f'expected a decimal string but got {dec_str} containing \'.\'')

    try:
        int(dec_str)
    except ValueError as err:
        raise ValueError(f'failed to convert {dec_str} to a number') from err

    neg = False
    if dec_str[0] == '-':
        neg = True
        dec_str = dec_str[1:]

    input_size = len(dec_str)
    bz_str = ''
    # case 1, purely decimal
    if input_size <= PRECISION:
        # 0. prefix
        bz_str = '0.'

        # set relevant digits to 0
        bz_str += '0' * (PRECISION - input_size)

        # set final digits
        bz_str += dec_str
    else:
        # inputSize + 1 to account for the decimal point that is being added
        dec_point_place = input_size - PRECISION

        bz_str = dec_str[:dec_point_place]  # pre-decimal digits
        bz_str += '.'  # decimal point
        bz_str += dec_str[dec_point_place:]  # pre-decimal digits

    if neg:
        bz_str = '-' + bz_str

    return float(bz_str)


def to_sdk_int(i: float) -> str:
    return str(int(i))


def from_sdk_int(int_str: str) -> int:
    return int(int_str)


def toPbTimestamp(dt: datetime):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


class ColoredFormatter(logging.Formatter):
    fmt = "%(asctime)s|%(levelname)s|%(funcName)s| %(message)s"

    white = "\x1b[97;20m"
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: fmt.format(green, reset),
        logging.INFO: fmt.format(cyan, reset),
        logging.WARNING: fmt.format(yellow, reset),
        logging.ERROR: fmt.format(red, reset),
        logging.CRITICAL: fmt.format(bold_red, reset),
    }

    def format(self, record: logging.LogRecord):
        """Formats a record for the logging handler.

        Args:
            record (logging.LogRecord): Represents an instance of an event being
                logged.
        """
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
        return formatter.format(record=record)


def clean_nested_dict(dictionary: Union[List, Dict, str]) -> Dict:
    """
    Takes a nested dictionnary with some values being string json values and convert it into a proper nested
    dictionary.

    Eg ::

        {
            "transaction_fee": "{\"denom\":\"unusd\",\"amount\":\"0\"}",
            "funding_payment": "0.000000000000000000",
            "realized_pnl": "0.000000000000000000",
            "bad_debt": "{\"denom\":\"unusd\",\"amount\":\"0\"}",
            "trader_address": "osmo1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
            "margin": "{\"denom\":\"unusd\",\"amount\":\"10\"}",
            "exchanged_position_size": "0.004999999999999500",
            "tx_hash": "12E496C996E39820B0807857CB7C19674BDD12DC8D789647D68C50BBB8C7D9CF"
        }

    becomes ::

        {
            "transaction_fee": {
                "denom": "unusd",
                "amount": "0"
            },
            "funding_payment": "0.000000000000000000",
            "realized_pnl": "0.000000000000000000",
            "bad_debt": {
                "denom": "unusd",
                "amount": "0"
            },
            "trader_address": "osmo1zaavvzxez0elundtn32qnk9lkm8kmcsz44g7xl",
            "margin": {
                "denom": "unusd",
                "amount": "10"
            },
            "exchanged_position_size": "0.004999999999999500",
            "tx_hash": "12E496C996E39820B0807857CB7C19674BDD12DC8D789647D68C50BBB8C7D9CF"
        }

    Args:
        dictionary (Union[List, Dict, str]): The dictionary to be converted.

    Returns:
        Dict: A converted dictionary.
    """

    if isinstance(dictionary, str):
        dictionary = json.loads(dictionary)

    for key, value in dictionary.items():
        if isinstance(value, str):
            if value[0] == "{" and value[-1] == "}":
                dictionary[key] = clean_nested_dict(value)
            elif value[0] == "[" and value[-1] == "]":
                try:
                    values_list = json.loads(value)
                    dictionary[key] = [
                        clean_nested_dict(v) for v in values_list]
                except ValueError:
                    dictionary[key] = value
            else:
                dictionary[key] = value

    return dictionary


# ----------------------------------------------------
# ----------------------------------------------------


def dict_keys_must_match(dict_: dict, keys: List[str]):
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.
    Alias for the 'element_counts_are_equal' function.

    dict_keys_must_match(dict_, keys)

    Example:
    - [0, 1, 1] and [1, 0, 1] compare equal.
    - [0, 0, 1] and [0, 1] compare unequal.

    """
    assert element_counts_are_equal(dict_.keys(), keys)


def element_counts_are_equal(
    first: Iterable[Any], second: Iterable[Any]
) -> Optional[bool]:
    """Asserts that two iterables have the same elements, the same number of
    times, without regard to order.

    Args:
        first (Iterable[Any])
        second (Iterable[Any])

    Returns:
        Optional[bool]: "passed" status. If this is True, first and second share
            the same element counts. If they don't the function will raise an
            AssertionError and return 'None'.
    """
    first_seq, second_seq = list(first), list(second)

    passed: Union[bool, None]
    try:
        first = collections.Counter(first_seq)
        second = collections.Counter(second_seq)
    except TypeError:
        # Handle case with unhashable elements
        differences = _count_diff_all_purpose(first_seq, second_seq)
    else:
        if first == second:
            passed = True
            return passed
        differences = _count_diff_hashable(first_seq, second_seq)

    if differences:
        standardMsg = "Element counts were not equal:\n"
        lines = ["First has %d, Second has %d:  %r" %
                 diff for diff in differences]
        diffMsg = "\n".join(lines)
        msg = "\n".join([standardMsg, diffMsg])
        passed = False
        assert passed, msg


_Mismatch = collections.namedtuple("Mismatch", "actual expected value")


def _count_diff_all_purpose(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements need not be hashable
    s, t = list(actual), list(expected)
    m, n = len(s), len(t)
    NULL = object()
    result = []
    for i, elem in enumerate(s):
        if elem is NULL:
            continue
        cnt_s = cnt_t = 0
        for j in range(i, m):
            if s[j] == elem:
                cnt_s += 1
                s[j] = NULL
        for j, other_elem in enumerate(t):
            if other_elem == elem:
                cnt_t += 1
                t[j] = NULL
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)

    for i, elem in enumerate(t):
        if elem is NULL:
            continue
        cnt_t = 0
        for j in range(i, n):
            if t[j] == elem:
                cnt_t += 1
                t[j] = NULL
        diff = _Mismatch(0, cnt_t, elem)
        result.append(diff)
    return result


def _count_diff_hashable(actual, expected):
    "Returns list of (cnt_act, cnt_exp, elem) triples where the counts differ"
    # elements must be hashable
    s, t = collections.Counter(actual), collections.Counter(expected)
    result = []
    for elem, cnt_s in s.items():
        cnt_t = t.get(elem, 0)
        if cnt_s != cnt_t:
            diff = _Mismatch(cnt_s, cnt_t, elem)
            result.append(diff)
    for elem, cnt_t in t.items():
        if elem not in s:
            diff = _Mismatch(0, cnt_t, elem)
            result.append(diff)
    return result


PROTOBUF_MSG_BASE_ATTRS: List[str] = (
    dir(message.Message)
    + ['Extensions', 'FindInitializationErrors', '_CheckCalledFromGeneratedFile']
    + ['_extensions_by_name', '_extensions_by_number']
)
"""PROTOBUF_MSG_BASE_ATTRS (List[str]): The default attributes and methods of
an instance of the 'protobuf.message.Message' class.
"""


def camel_to_snake(camel: str):
    return ''.join(
        ['_' + char.lower() if char.isupper() else char for char in camel]
    ).lstrip('_')


def dict_keys_from_camel_to_snake(d):
    """
    Transform all keys from the dictionary from camelcase to snake case.

    Args:
        d (dict): The dictionary to transform

    Returns:
        dict: The dictionary transformed
    """
    if isinstance(d, list):
        return [
            dict_keys_from_camel_to_snake(
                i) if isinstance(i, (dict, list)) else i
            for i in d
        ]
    return {
        camel_to_snake(a): dict_keys_from_camel_to_snake(b)
        if isinstance(b, (dict, list))
        else b
        for a, b in d.items()
    }


def deserialize(pb_msg: message.Message, no_sdk_transformation: bool = False) -> dict:
    """Deserializes a proto message into a dictionary.

    - sdk.Dec values are converted to floats.
    - sdk.Int values are converted to ints.
    - Missing fields become blank strings.

    Args:
        pb_msg (protobuf.message.Message)
        no_sdk_transformation (bool): Wether to bypass the sdk transformation. Default to False

    Returns:
        dict: 'pb_msg' as a JSON-able dictionary.
    """
    if not isinstance(pb_msg, message.Message):
        return pb_msg
    custom_dtypes: Dict[str, bytes] = {
        str(field[1]): field[0].GetOptions().__getstate__().get("serialized", None)
        for field in pb_msg.ListFields()
    }
    serialized_output = {}
    expected_fields: List[str] = list(pb_msg.DESCRIPTOR.fields_by_name.keys())

    for _, attr in enumerate(expected_fields):
        attr_search = pb_msg.__getattribute__(attr)
        custom_dtype = custom_dtypes.get(str(attr_search))

        if custom_dtype is not None:
            if "sdk/types.Dec" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = float(
                        pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = utils.from_sdk_dec(
                        pb_msg.__getattribute__(attr)
                    )
            elif "sdk/types.Int" in str(custom_dtype):
                if no_sdk_transformation:
                    serialized_output[str(attr)] = int(
                        pb_msg.__getattribute__(attr))
                else:
                    serialized_output[str(attr)] = utils.from_sdk_int(
                        pb_msg.__getattribute__(attr)
                    )
            elif "Int" in str(custom_dtype):  # Used for sdk.Coin message normalization
                serialized_output[str(attr)] = int(
                    pb_msg.__getattribute__(attr))
            else:
                val = pb_msg.__getattribute__(attr)
                if hasattr(val, '__len__') and not isinstance(val, str):
                    updated_vals = []
                    for v in val:
                        updated_vals.append(deserialize(v))
                    serialized_output[str(attr)] = updated_vals
                else:
                    serialized_output[str(attr)] = deserialize(val)
        elif custom_dtype is None and not attr_search:
            if str(attr_search) == "[]":
                serialized_output[str(attr)] = []
            else:
                serialized_output[str(attr)] = attr_search
        else:
            serialized_output[str(attr)] = deserialize(
                pb_msg.__getattribute__(attr))

    return serialized_output


def deserialize_exp(proto_message: message.Message) -> dict:
    """
    Take a proto message and convert it into a dictionnary.
    sdk.Dec values are converted to be consistent with txs.

    Args:
        proto_message (protobuf.message.Message)

    Returns:
        dict
    """
    output = json_format.MessageToDict(proto_message)

    is_sdk_dec = {
        field.camelcase_name: "types.Dec" in str(field.GetOptions())
        for field in proto_message.DESCRIPTOR.fields
    }

    for field in proto_message.DESCRIPTOR.fields:
        if field.message_type is not None:
            # This is another proto object
            try:
                output[field.camelcase_name] = deserialize_exp(
                    proto_message.__getattribute__(field.camelcase_name)
                )
            except AttributeError:
                output[field.camelcase_name] = output[field.camelcase_name]

        elif is_sdk_dec[field.camelcase_name]:
            output[field.camelcase_name] = utils.from_sdk_dec(
                output[field.camelcase_name]
            )

    return dict_keys_from_camel_to_snake(output)
