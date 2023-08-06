# Split secrets into T pieces. The secret can be recovered by recombining any D pieces.

[Overview (wikipedia)](https://wikipedia.org/wiki/Secret_sharing)

This module implements:

- `block-wise SSS`: a block-wise version of [Shamir's secret sharing](https://wikipedia.org/wiki/Shamir%27s_secret_sharing).
    Full implementation details on [https://secret-splitter.com](https://secret-splitter.com).

Splitting is done by:

1. Apply a random mask to the secret
1. For each block of the mask, generate a polynomial of degree D-1
1. A piece consists of the masked secret and one point of each polynomial

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
