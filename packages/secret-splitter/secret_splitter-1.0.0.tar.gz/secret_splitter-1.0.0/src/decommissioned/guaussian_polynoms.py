"""Shamir's secret sharing (SSS) implementation

Split a digital secret into T pieces.
The original secret can be recovered by recombining any D pieces.

wikipedia.org/wiki/Shamir%27s_secret_sharing

Full implementation details: secret-splitter.com

Splitting is done by:

1. Apply a random mask to the secret
2. For each byte of the mask, generate a polynomial of degree D-1
3. A piece consists of the masked secret and one point of each polynomial

Recovering is done by:

1. Collect D pieces: D polynomials for each byte of the mask
2. Interpolate back the bytes of the mask
3. Recover the secret by re-applying the mask to the masked version

A puzzle piece is a [yaml](https://yaml.org) serialisation of the following mapping:

```yaml
# string, tells if the secret encoded is a string encoded as UTF-8 ("utf-8") or a raw stream of bytes ("none")
encoding: utf-8

# one  puzzle piece, exact format depending on the implementation
# this implementation stores a sequence of [point, value] items, one per block of the secret 
# Flow-sequence format preferred to keep it on one line
puzzle piece: [[1,258],[1,3]]

# base64 representation of the result of the mask XOR the byte representation of the secret
encoded secret: YXo=
```
"""

from base64 import b64encode, b64decode
from math import prod
from operator import itemgetter
from secrets import randbits, token_bytes
from statistics import NormalDist


from src.common import InvalidPieces, InvalidParam, xor

NAME = 'guaussian polynoms'


def split(secret, D, T=None, block_size=2, encoding=None, **kwargs):
    """Split a secret into T pieces, D required to recover it

    T: defaults to D, should be >= D
    block_size: 
    encoding: "utf-8" by default for string secrets."""
    if D < 2:
        raise InvalidParam(
            'Minimum amount of pieces required to solve the puzzle should be at least 2')
    if T is None:
        T = D
    if T < D:
        raise InvalidParam(
            'Total amount of pieces should be greater than the minimal amount required to solve')
    if isinstance(secret, bytes):
        if encoding is not None and encoding.lower() != 'none':
            raise InvalidParam(
                f'Secret is already binary, cannot re-encode with {encoding}')
    elif isinstance(secret, str):
        if encoding is None:
            encoding = 'utf-8'
        elif encoding == 'none':
            raise InvalidParam(
                'Secrets in string format have to be encoded, but got encoding="none". '
                'Specify either a valid encoding, or nothing at all to use "utf-8".'
            )
        secret = secret.encode(encoding)
    else:
        raise InvalidParam(
            f'Unrecognized secret format, expected bytes or str, got {type(secret)}')
    if T < D:
        raise InvalidParam(
            'Total number of pieces should be bigger than the minimal amount required to decode. '
            f'Got total={T}, min={D}')
    mask = token_bytes(len(secret))
    secret = b64encode(xor(mask, secret)).decode('utf-8')

    pieces = zip(*(split_piece(mask[i: i+block_size], D, T, **kwargs)
                 for i in range(0, len(mask), block_size)))

    if encoding is None or encoding == 'none':
        return ({"puzzle piece": piece, "encoded secret": secret, 'algorithm': NAME} for piece in pieces)
    return ({"puzzle piece": piece, "encoded secret": secret, "encoding": encoding, 'algorithm': NAME}
            for piece in pieces)


def split_piece(block, D, T, **kwargs):
    """Split a single encoded block into pieces"""
    # pylint: disable=missing-kwoa
    pieces = tuple(generate_polynomial(block, D, **kwargs))
    yield from pieces
    for i in range(D+1, T+1):
        yield (i, interpolate(pieces, i))


def solve(pieces, block_size=2, masked_secret=None, encoding=None):
    """Takes a sequence of pieces and return the decoded secret

    pieces: sequence of pieces, the direct yaml deserialisation of the standard format:
    ```[{
        "encoding": "utf-8",  # optional, if specified: encoding of the secret
        "puzzle piece": [[1, 258], [1,3]],  # one (point, value) pair per block of the mask
        "encoded secret": "Yxo="  # base64 encoded masked secret
    }, ...]```

    masked_secret: optional, override the encoded masked_secret to use if all pieces don't share the same one.
        This can happen if one of the pieces was tempered with.

    encoding: optional, override the encoding used to decode the secret.
        Default behaviour is to use the encoding provided in the pieces, if present.
        Use 'none' to disable decoding.
    """
    pieces = tuple(
        pieces)   # consume iterators as we will need to iterate several times
    if len(pieces) == 0:
        raise InvalidPieces("Need at least one piece to decode the secret")
    if masked_secret is None:
        secrets = set((piece["encoded secret"] for piece in pieces))
        if len(secrets) > 1:
            raise InvalidPieces(
                "Not all pieces have the same encoded secret. Are you sure they all represent the same secret? "
                "If yes, please specify the encoded secret to use.")
        masked_secret, *_ = secrets
    if encoding is None:
        encodings = set((piece.get("encoding", None)
                        for piece in pieces)) - {None}
        if len(encodings) > 1:
            raise InvalidPieces(
                "Not all pieces have the same encoding. Are you sure they all represent the same secret? "
                "If yes, please override the encoding to use. Use `none` to disable.")
        if len(encodings) == 1:
            encoding, *_ = encodings
        # else: no custom encoding provided, keep default of None
    mask = decode_mask((piece["puzzle piece"] for piece in pieces), block_size)
    if encoding is None or encoding.lower() == 'none':
        return xor(mask, b64decode(masked_secret.encode('utf-8')))
    return xor(mask, b64decode(masked_secret.encode('utf-8'))).decode(encoding)


def decode_mask(puzzle_pieces, block_size):
    """
    There should be at least D pieces.
    One piece is a sequence of N points, one per byte of the mask.
    Point i of each of the D pieces together are points of a polynomial taking the value of byte i of the mask at 0.
    """
    try:
        return b''.join(
            int.to_bytes(int(round(interpolate(points, 0), 0)),
                         block_size, 'little')
            for points in zip(*puzzle_pieces)
        )
    except OverflowError as e:
        raise InvalidPieces(
            'Cannot decode mask as some of the outputs are not in the valid range. '
            "Are you sure all pieces are for the same secret? If yes, you don't have enough to decode it."
        ) from e


def interpolate(points, at):
    """Perform Lagrange interpolation

    points: sequence of (x_values, y_values)
    """
    return sum((y_i * factor
                for (_, y_i), factor in zip(points, interpolation_factors(map(itemgetter(0), points), at))))


def interpolation_factors(x_values, at):
    r"""Lagrange interpolation factors to compute the value of a polynomial at `at`

    $$ L_i = \prod_{1 \leq j \leq n , j \neq i}\frac{X_j - X_0}{X_j-X_i} $$
    """
    x_values = tuple(x_values)  # consume iterators for the double loop
    for i, x_i in enumerate(x_values):
        yield prod(((x_j - at) / (x_j - x_i) for (j, x_j) in enumerate(x_values) if i != j))


def normal_sample(bits=50):
    """Generate a standard normal sample

    bits: Number of random bits used to sample the initial uniform value.
    Defaults to 50 as 1/2**50 is approx. 1e-15, python float precision.
    """
    uniform = randbits(bits)
    while uniform == 0:
        uniform = randbits(bits)
    return NormalDist().inv_cdf(uniform / 2**bits)


def generate_polynomial(value_at_0, D, *, sigma=100, bits=50):
    """Generate D points of a random polynomial of degree D-1 for the given intercept

    Points are gerenated for values i=1, ..., D-1 from a normal distribution of standard dev sigma / L_i.
    L_i being the Lagrange interpolation factor used to interpolate the value of the polynomial at D.
    Value at D is interpolated from them and the intercept.

    Returns: ((1, y_1),..., (D, y_D)) <- the intercept is skipped
    """
    if isinstance(value_at_0, bytes):
        value_at_0 = int.from_bytes(value_at_0, 'little')
    value_at_d = 0
    for i, L_i in enumerate(interpolation_factors(range(0, D), D)):
        if i == 0:
            # yield (i, value_at_0) -> this is the intercept we want to hide, don't return it!
            value_at_d += value_at_0 * L_i
        else:
            y_i = normal_sample(bits) * sigma / L_i
        # no need to take abs(L_i) as -1 * normal sample is still a normal sample
            yield (i, y_i)
            value_at_d += y_i * L_i
    yield (D, value_at_d)
