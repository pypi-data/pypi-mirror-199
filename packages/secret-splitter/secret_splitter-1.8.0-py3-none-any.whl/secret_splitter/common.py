"""Error classes"""

import sys


class InvalidPieces(ValueError):
    """Thrown when the pieces provided to decode() are invalid"""


class InvalidParam(ValueError):
    """Thrown when user-supplied params are invalid"""


def xor(left: bytes, right: bytes):
    """xor two byte strings"""
    if len(left) != len(right):
        raise ValueError(
            f'Both args must be of same length. Got {len(left)} and {len(right)}')
    return int.to_bytes(
        int.from_bytes(left, sys.byteorder) ^ int.from_bytes(
            right, sys.byteorder),
        len(left),
        sys.byteorder)
