"""tests for src/__main__.py
"""

from itertools import combinations

from src.secret_splitter.common import InvalidParam, InvalidPieces

SIZE = 128


def run_on(package, **kwargs):
    """Check that a package properly implements split and solve"""
    try:
        pieces = package.split(b'my super binary secret', 10, 9, **kwargs)
    except InvalidParam:
        pass
    else:
        raise ValueError('should have failed: T<D')

    pieces = tuple(package.split('my super binary secret',
                   2, 3, encoding='utf-8', **kwargs))
    for piece in pieces:
        assert piece['algorithm'] == package.NAME
    assert len(pieces) == 3
    assert package.solve(
        pieces, masked_secret=pieces[0]['encoded secret'], encoding='none', **kwargs
    ) == b'my super binary secret', \
        package.solve(pieces, **kwargs)

    pieces = tuple(package.split(b'my super binary secret', 2, 3, **kwargs))
    assert len(pieces) == 3
    assert package.solve(pieces, encoding='utf-8', **kwargs) == 'my super binary secret', \
        package.solve(pieces, **kwargs)

    pieces = tuple(package.split('my super string secret', 3, 4, **kwargs))
    assert package.solve(pieces, **kwargs) == 'my super string secret'
    for sub_pieces in combinations(pieces, 3):
        assert package.solve(sub_pieces, **kwargs) == 'my super string secret'
    for sub_pieces in combinations(pieces, 2):
        try:
            assert package.solve(
                sub_pieces, **kwargs) != 'my super string secret'
        except InvalidPieces:
            pass
