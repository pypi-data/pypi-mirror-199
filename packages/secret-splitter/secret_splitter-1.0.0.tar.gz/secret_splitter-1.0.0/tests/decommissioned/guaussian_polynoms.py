"""tests for src/__main__.py
"""

import yaml

from src.decommissioned.guaussian_polynoms import interpolate, generate_polynomial, solve
import src.decommissioned.guaussian_polynoms as package
from tests.suite import run_on

SIZE = 128

if __name__ == '__main__':
    assert interpolate(((1, 1), (2, 4), (3, 9)), 0) == 0, interpolate(
        ((1, 1), (2, 4), (3, 9)), 0)
    assert interpolate(((1, 1), (2, 4), (3, 9)), 4) == 16, interpolate(
        ((1, 1), (2, 4), (3, 9)), 4)

    pieces = tuple(yaml.safe_load_all("""
---
puzzle piece: [[1, 1], [1, 1]]
encoded secret: WW8=
---
puzzle piece: [[2, 2], [2, 2]]
encoded secret: WW8=
encoding: utf-8
    """))
    assert solve(pieces, encoding='none', block_size=1) == b'Yo'
    assert solve(pieces, block_size=1) == 'Yo'

    polynomial = tuple(generate_polynomial(
        value_at_0=b'\x04', D=10, sigma=2, bits=4))
    assert len(polynomial) == 10
    assert round(interpolate(polynomial, 0), 14) == 4

    run_on(package)
