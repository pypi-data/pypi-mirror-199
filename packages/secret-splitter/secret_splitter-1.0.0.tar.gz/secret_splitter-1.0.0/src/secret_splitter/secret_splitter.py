"""High-level entry point over all algorithms
"""
from . import block_sss
from .common import InvalidPieces

ALGORITHMS = {
    block_sss.NAME: block_sss,
}

DEFAULT = block_sss.NAME


def split(secret, D, T, algorithm=None, **kwargs):
    """Split a secret into T>=D pieces, D required to recover it"""
    if algorithm is None:
        algorithm = DEFAULT
    return ALGORITHMS[algorithm].split(secret, D, T, **kwargs)


def solve(pieces, algorithm=None, **kwargs):
    """Retrieve and decodes a secret from raw deserialized pieces."""
    if len(pieces) < 2:
        raise InvalidPieces('Need at least 2 pieces to retrieve the secret')
    if algorithm is None:
        algorithms = set((piece.get("algorithm", None)
                          for piece in pieces)) - {None}
        if len(algorithms) > 1:
            raise InvalidPieces(
                "Not all pieces have the same algorithm. Are you sure they all represent the same secret? "
                "If yes, please override the algorithm to use. \n"
                f"Supported algorithms: {set(ALGORITHMS.keys())}")
        if len(algorithms) == 0:
            raise InvalidPieces(
                "None of the pieces specify the algorithm. Are you sure they all represent the same secret? "
                "If yes, please override the algorithm to use.\n"
                f"Supported algorithms: {set(ALGORITHMS.keys())}")
        algorithm, *_ = algorithms
    return ALGORITHMS[algorithm].solve(pieces, **kwargs)
