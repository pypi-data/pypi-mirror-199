"""tests for src/__main__.py
"""

import yaml
import src.secret_splitter.block_sss as package
from src.secret_splitter.block_sss import (generate_polynomial, interpolate,
                                           solve)
from tests.secret_splitter.suite import run_on

if __name__ == '__main__':
    assert interpolate(((1, 1), (2, 4), (3, 9)), 0, field_size=257) == 0
    assert interpolate(((1, 1), (2, 4), (3, 9)), 4, field_size=257) == 16

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
        value_at_0=b'\x04', D=10, block_size=2, field_size=65537))
    assert len(polynomial) == 10
    assert round(interpolate(polynomial, 0, field_size=65537), 0) == 4, round(
        interpolate(polynomial, 0, field_size=65537), 14)

    run_on(package, block_size=1)
    run_on(package, block_size=2)
    run_on(package, block_size=3)
