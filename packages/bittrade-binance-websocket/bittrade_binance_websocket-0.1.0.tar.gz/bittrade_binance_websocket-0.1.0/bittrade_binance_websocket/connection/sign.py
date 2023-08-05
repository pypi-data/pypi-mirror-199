from enum import Enum
import hashlib
import hmac
from typing import Any, Dict, Tuple, Union, cast
from urllib.parse import urlencode

from expression import curry_flip


def to_sorted_qs(values: Union[Dict[str, Any], Any]) -> Tuple[Tuple[str, Any]]:
    """
    Returns a tuple of sorted key-value pairs from the given dictionary.

    Args:
    - values: A dictionary containing key-value pairs.

    Returns:
    - A tuple of sorted key-value pairs, where each pair is represented as a tuple of two elements,
    the first being the key and the second being the corresponding value.
    """
    sorted_tuple = tuple()
    keys = sorted(values)
    for key in keys:
        value = values[key]
        if isinstance(value, Enum):
            value = cast(Enum, value).value

        # remove None
        if value:
            sorted_tuple = sorted_tuple + ((key, value,),)
    
    return sorted_tuple

def encode_query_string(params: Tuple):
    """
    Returns the URL-encoded string representation of the given tuple of key-value pairs.

    Args:
    - params: A tuple of key-value pairs.

    Returns:
    - The URL-encoded string representation of the given tuple of key-value pairs.
    """
    encoded = urlencode(params)
    return encoded

@curry_flip(1)
def get_signature(qs: str, secret: str):
    """
    Returns the SHA-256 HMAC signature of the given query string using the provided secret key.

    Args:
    - qs: The query string to sign.
    - secret: The secret key to use for signing.

    Returns:
    - The SHA-256 HMAC signature of the given query string using the provided secret key.
    """
    signed = hmac.new(secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256)
    return signed.hexdigest()