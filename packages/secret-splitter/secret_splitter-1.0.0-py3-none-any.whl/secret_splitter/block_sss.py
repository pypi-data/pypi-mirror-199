"""Shamir's secret sharing (SSS) block-wise implementation: one polynom per block of n bytes of the secret.

Parameters:
    block_size (default 2): size in bytes of the individual blocks. 

Overview of the algorithm: https://wikipedia.org/wiki/Shamir%27s_secret_sharing
Full implementation details: https://secret-splitter.com

Splitting is done by:

1. Apply a random mask to the secret
2. For each block of the mask, generate a polynomial of degree D-1
3. A piece consists of the masked secret and one point of each polynomial

Recovering is done by:

1. Collect D pieces: D polynomials for each block of the mask
2. Interpolate the points to retrieve the blocks of the mask
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

# name of the algorithm used for splitting
algorithm: block-wise SSS

# different algorithms might add additional information required for recovering the secret.
```

Working on blocks makes the algorithm linear in the number of bytes of the secret rather than exponential.
Otherwise the search for the first prime bigger than the secret adds a 2^(secret length / 2) complexity.

Computations are done over the finite field of size the next prime number after 256**block_size.
Only block sizes 1, 2, and 3 are implemented, allowing for splitting secrets into up to 16 million pieces.

To support larger number of pieces, extend PRIME_OFFSET.

Secret & mask are little-endian.
If the length of the secret is not a multiple of block size, it can safely be padded with zeroes.
"""

from base64 import b64decode, b64encode
from math import prod
from operator import itemgetter
from secrets import randbits, token_bytes

from .common import InvalidParam, InvalidPieces, xor

BYTE_SIZE = 256

# offset to the next prime after 256**block_size, for each block_size
PRIME_OFFSET = [None, 1, 1, 43]

NAME = 'block-wise SSS'


# pylint: disable=too-many-branches
def split(secret, D, T=None, block_size=2, encoding=None):
    """Split a secret into T>=D pieces, D required to recover it. Encodes strings with specified encoding (def utf-8)"""
    if block_size < 1:
        raise InvalidParam('block size should be at least 1')
    if block_size > len(PRIME_OFFSET):
        raise InvalidParam(
            f'block size only supported up to {len(PRIME_OFFSET)}')
    field_size = BYTE_SIZE**block_size + \
        PRIME_OFFSET[block_size]  # needs to be prime

    if D < 2:
        raise InvalidParam(
            'Minimum amount of pieces required to solve the puzzle should be at least 2')
    if T is None:
        T = D
    if T < D:
        raise InvalidParam(
            'Total amount of pieces should be greater than the minimal amount required to solve')
    while T >= field_size and block_size < len(PRIME_OFFSET):
        block_size += 1
        field_size = BYTE_SIZE**block_size + \
            PRIME_OFFSET[block_size]  # needs to be prime
    if T >= field_size:
        raise InvalidParam(
            f'Block size {block_size} only allows for up to {BYTE_SIZE**block_size} pieces')
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

    pieces = zip(*(
        split_block(mask[i: i+block_size], D, T,
                    block_size=block_size, field_size=field_size)
        for i in range(0, len(mask), block_size)))

    if encoding is None or encoding == 'none':
        return ({
            "puzzle piece": piece,
            "encoded secret": secret,
            "algorithm": NAME,
            "block size": block_size} for piece in pieces)
    return ({
        "puzzle piece": piece,
        "encoded secret": secret,
        "encoding": encoding,
        "algorithm": NAME,
        "block size": block_size} for piece in pieces)


def split_block(block, D, T, *, block_size, field_size):
    """Split a single encoded block into pieces"""
    # pylint: disable=missing-kwoa
    pieces = tuple(generate_polynomial(
        block, D, block_size=block_size, field_size=field_size))
    yield from pieces
    for i in range(D+1, T+1):
        yield (i, interpolate(pieces, i, field_size=field_size))


def solve(puzzle_pieces, block_size=2, masked_secret=None, encoding=None):
    """Retrieve and decodes a secret from raw deserialized pieces.

    masked_secret, encoding: override the values read from the pieces.
    """
    field_size = BYTE_SIZE**block_size + PRIME_OFFSET[block_size]
    puzzle_pieces = tuple(
        puzzle_pieces)   # consume iterators as we will need to iterate several times
    if len(puzzle_pieces) == 0:
        raise InvalidPieces("Need at least one piece to decode the secret")
    if masked_secret is None:
        secrets = set((piece["encoded secret"] for piece in puzzle_pieces))
        if len(secrets) > 1:
            raise InvalidPieces(
                "Not all pieces have the same encoded secret. Are you sure they all represent the same secret? "
                "If yes, please specify the encoded secret to use.")
        masked_secret, *_ = secrets
    masked_secret = b64decode(masked_secret.encode('utf-8'))
    if encoding is None:
        encodings = set((piece.get("encoding", None)
                        for piece in puzzle_pieces)) - {None}
        if len(encodings) > 1:
            raise InvalidPieces(
                "Not all pieces have the same encoding. Are you sure they all represent the same secret? "
                "If yes, please override the encoding to use. Use `none` to disable.")
        if len(encodings) == 1:
            encoding, *_ = encodings
        # else: no custom encoding provided, keep default of None
    mask = decode_mask(puzzle_pieces, block_size, field_size)
    if encoding is None or encoding.lower() == 'none':
        # works because little-endian
        return xor(mask[:len(masked_secret)], masked_secret)
    try:
        return xor(mask[:len(masked_secret)], masked_secret).decode(encoding)
    except UnicodeDecodeError as e:
        raise InvalidPieces(
            'Cannot decode secret as some of the outputs are not in the valid range. '
            "Are you sure all pieces are for the same secret? If yes, you don't have enough to decode it."
        ) from e


def decode_mask(puzzle_pieces, block_size, field_size):
    """Perform the Lagrange interpolations to retrieve each block of the mask"""
    try:
        return b''.join(
            int.to_bytes(
                int(interpolate(points, 0, field_size=field_size)), block_size, 'little')
            for points in zip(*(piece["puzzle piece"] for piece in puzzle_pieces))
        )
    except OverflowError as e:
        raise InvalidPieces(
            'Cannot decode mask as some of the outputs are not in the valid range. '
            "Are you sure all pieces are for the same secret? If yes, you don't have enough to decode it."
        ) from e


def interpolate(points, at, *, field_size):
    """Lagrange interpolation on the field_size field"""
    if not isinstance(points, (tuple, list)):
        points = tuple(points)
    return sum((
        y_i * factor
        for (_, y_i), factor in zip(points, interpolation_factors(map(itemgetter(0), points), at, field_size))
    )
    ) % field_size

    # assert v%field_size >= 0, v
    # assert abs(v-round(v, 0)) < 0.01, v
    # return v


def interpolation_factors(x_values, at, field_size):
    r"""Lagrange interpolation factors to compute the value of a polynomial at `at` in the field_size field

    $$ L_i = \prod_{1 \leq j \leq n , j \neq i}\frac{X_j - X_0}{X_j-X_i} $$

    Insted of dividing, by X_j-X_i, multiply by the modular inverse = X_j-X_i % prime as prime is prime
    """
    if not isinstance(x_values, (tuple, list)):
        x_values = tuple(x_values)  # consume iterators for the double loop
    for i, x_i in enumerate(x_values):
        yield prod(((x_j - at) * inverse(x_j - x_i, field_size) for (j, x_j) in enumerate(x_values) if i != j)
                   ) % field_size


def bezout_identity(big, small):
    """x and y such that x * big + y * small = 1, assuming 1 is the gcd of big and small"""
    quotient = big//small
    result = big % small
    if result == 1:
        return (1, -quotient)
    x, y = bezout_identity(small, result)
    return (y, x - quotient * y)


def inverse(num, prime):
    """Inverse of num modulo prime, much faster than num**(prime-2) for big primes"""
    if num == 1:
        return 1
    return bezout_identity(prime, num % prime)[1] % prime


def rand_int(block_size, field_size):
    """True uniform samples in [0, field_size[

    We have to draw 8*block_size+1 bytes to include field_size-1.
    There is a (8**block_size-1) / (2*8**(block_size+1)) chance that the number is too big and we need to redraw.
    """
    y_i = randbits(8*block_size + 1)
    while y_i >= field_size:
        y_i = randbits(8*block_size + 1)
    return y_i


def generate_polynomial(value_at_0, D, *, block_size, field_size):
    """Generate D points of a random polynomial of degree D-1 for the given intercept

    y-values are gerenated for x-values i=1, ..., D-1 from a uniform distribution in [0, field_size[.
    Value at D is interpolated from them and the intercept.

    Returns: ((1, y_1),..., (D, y_D)) <- the intercept is skipped
    """
    if isinstance(value_at_0, bytes):
        value_at_0 = int.from_bytes(value_at_0, 'little')
    value_at_d = 0
    for i, L_i in enumerate(interpolation_factors(range(0, D), D, field_size)):
        if i == 0:
            # yield (i, value_at_0) -> this is the intercept we want to hide, don't return it!
            value_at_d += value_at_0 * L_i
        else:
            y_i = rand_int(block_size, field_size)
            yield (i, y_i)
            value_at_d += y_i * L_i
    yield (D, value_at_d % field_size)
