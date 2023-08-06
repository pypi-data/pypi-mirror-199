# Secret Splitter

- Turn your digital secrets into digital puzzles (literally).
- Distribute the pieces among a group of people.
- Anyone can decode the secret by collecting all the pieces back.
- But if even one piece is missing, all they have is random data.
- You then trust that group of people to only share their pieces for a good reason.
- You can add resilience by allowing for some pieces to be missing / corrupt.


[Overview (wikipedia)](https://wikipedia.org/wiki/Secret_sharing)

This module implements:

- `block-wise SSS`: a block-wise version of [Shamir's secret sharing](https://wikipedia.org/wiki/Shamir%27s_secret_sharing).
    Full implementation details on [https://secret-splitter.com](https://secret-splitter.com).

    Working on blocks makes the algorithm linear in the number of bytes of the secret rather than exponential.

## Splitting

1. Apply a random mask to the secret
1. For each block of the mask, generate a polynomial of degree D-1
1. A piece consists of the masked secret and one point of each polynomial

## Recovery

1. Collect D pieces: D polynomials for each block of the mask
2. Interpolate the points to retrieve the blocks of the mask
3. Recover the secret by re-applying the mask to the masked version

## Standard piece format

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

## Installation

- Using PyPi

    `python3 -m pip install secret-splitter`

- From source

    `git clone https://git.sr.ht/~retzoh/secret-splitter-py && cd secret-splitter-py && python3 -m pip install .`

## Usage

- Command line

    `echo "secret" | python3 -m secret_splitter split 3 2 --stdin | python3 -m secret_splitter solve`

    See `python3 -m secret_splitter --help` for all options.

- Python script

    ```python
    >>> from secret_splitter import split, solve
    >>> pieces = split('secret', 3, 2)
    >>> secret = solve(pieces)
    ```

## Contibute

Contributions of new algorithms are welcome as long as they pass the test & lint suite.

To add a new algorithm, create src/secret_splitter/algorithm.py and add it to ALGORITHMS in
[src/secret_splitter/secret_splitter.py](https://git.sr.ht/~retzoh/secret-splitter-py/tree/master/item/src/secret_splitter/secret_splitter.py).

Install [redo](https://redo.readthedocs.io) and run `redo` from the root folder to run the tests.
