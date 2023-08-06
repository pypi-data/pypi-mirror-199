"""Test src/common.py"""

from secrets import token_bytes

from src.secret_splitter.common import xor

if __name__ == "__main__":
    SIZE = 128

    secret = token_bytes(SIZE)
    mask = token_bytes(SIZE)

    assert xor(mask, mask) == b'\x00' * len(mask)
    assert xor(xor(mask, secret), mask) == secret
