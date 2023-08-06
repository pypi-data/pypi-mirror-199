"""CLI interface for secret-splitter

Use `split -h` or `solve -h` for additinal help on sub-commands.
Use `doc ALGORITHM` to display additional info & parameters of a specific algorithm.

Supported algorithms:

    - "block-wise SSS"
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
from getpass import getpass
import io
from pathlib import Path
import sys

import yaml

from .secret_splitter import split, solve, ALGORITHMS, DEFAULT


def main():
    """CLI entry point"""
    if len(sys.argv) == 1:
        sys.argv += ['-h']
    parser = ArgumentParser(
        description="Split secrets into T pieces, or recover split secrets by recombining any D pieces.",
        epilog=__doc__, formatter_class=RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title='command', dest='command')

    split_cmd = subparsers.add_parser('split',
                                      description='Read a secret from user input, file or stdin. '
                                      'Write the pieces to a stdout (concatenated) or a folder.',
                                      help='Read a secret from user input, file or stdin. '
                                      'Write the pieces to a stdout (concatenated) or a folder.')
    split_cmd.add_argument(
        'TOTAL', type=int, help='Total number of pieces to produce')
    split_cmd.add_argument(
        'REQUIRED', type=int, help='Minimum amount of pieces required to retrieve the secret')
    input_group = split_cmd.add_mutually_exclusive_group(required=False)
    input_group.add_argument('--input', '-i', '--file', '-f', metavar='FILE', type=FileType('rb'),
                             help='Read secret from file instead of user input.')
    input_group.add_argument('--stdin', '-s', action='store_true',
                             help='Read secret from stdin instead of user input.')
    split_cmd.add_argument(
        '--output', '-o', metavar='DIR',
        help='Output folder for the pieces, created if missing. Concatenated and written to stdout if omitted.')
    split_cmd.add_argument('--encoding', '-e',
                           help='Treat input as text in specified encoding. If "none" or omitted, treat as bytes.')
    split_cmd.add_argument('--piece_name_pattern', '-p', default='secret-splitter_piece_{}.yaml',
                           help='Pattern to use to generate the names of the pieces when --output is provided')
    split_cmd.add_argument(
        '--algorithm', '--algo', '-a', choices=list(ALGORITHMS.keys()), default=DEFAULT,
        help=f'algorithm to use for secret splitting, default "{DEFAULT}".')

    solve_cmd = subparsers.add_parser(
        'solve',
        description='Read pieces from stdin (concatenated) or a folder. Write the secret to stdout.',
        help='Read pieces from stdin (concatenated) or a folder. Write the secret to stdout.')
    solve_cmd.add_argument(
        '--input', '-i', '--dir', '-d', metavar='DIR',
        help='Read pieces from directory instead of user input. '
        'EVERY file in the director is assumed to be one piece.')
    solve_cmd.add_argument(
        '--output', '-o', '--file', '-f', metavar='FILE', type=FileType('w'),
        help='Write decoded secret to file instead of stdout.')
    solve_cmd.add_argument(
        '--encoding', '-e',
        help='Override the encoding used to output the secret. Default is inferred from the pieces.')
    solve_cmd.add_argument('--piece_name_pattern', '-p', default='secret-splitter_piece_*.yaml',
                           help='Pattern to use when looking for pieces in DIR when --input is provided')
    solve_cmd.add_argument(
        '--masked_secret', metavar='BASE64_ENCODED_SECRET',
        help='Override the masked secret inferred from the pieces.')
    solve_cmd.add_argument(
        '--algorithm', '--algo', '-a',
        choices=list(ALGORITHMS.keys()),
        help='Algorithm to use for recovering a secret, default inferred from the pieces.')

    doc_cmd = subparsers.add_parser(
        'doc',
        description='Extended documentation for a specific algorithm and its additional parameters.',
        help='Extended documentation for a specific algorithm and its additional parameters.')
    doc_cmd.add_argument(
        'algorithm', choices=list(ALGORITHMS.keys()),
        help='algorithm to use for recovering a secret, default inferred from the pieces')

    args, pass_through = parser.parse_known_args()

    if args.command == 'doc':
        print(ALGORITHMS[args.algorithm].__doc__)
        return 0

    kwargs = {'encoding': args.encoding, 'algorithm': args.algorithm}

    if len(pass_through) > 0:
        kwargs.update(
            dict(zip(map(lambda s: s.lstrip('-'), pass_through[::2]), pass_through[1::2])))

    if args.command == 'split':
        return do_split(args, kwargs)

    assert args.command == 'solve'
    return do_solve(args, kwargs)


def do_split(args, kwargs):
    """Read secret from the appropriate input, split it, and write it to appropriate output
    """
    if args.stdin or args.input is not None:
        input_stream = sys.stdin.buffer if args.stdin else args.input
        if args.encoding is None or args.encoding.lower() == 'none':
            secret = input_stream.read()
        else:
            secret = io.TextIOWrapper(
                input_stream, encoding=args.encoding).read()
    else:
        secret = getpass("Input secret (caracters won't be visible): ")
        if secret != getpass('Repeat secret: '):
            print("Secret missmatch, aborting")
            return 1

    pieces = split(secret, args.REQUIRED, args.TOTAL, **kwargs)

    if args.output is None:
        yaml.safe_dump_all(pieces, sys.stdout,
                           explicit_start=True, encoding='utf-8')
    else:
        folder = Path(args.output)
        if not folder.exists():
            folder.mkdir(parents=True)
        for i, piece in enumerate(pieces):
            (folder / args.piece_name_pattern.format(i)).write_bytes(
                yaml.safe_dump(piece, explicit_start=True, encoding='utf-8'))
    return 0


def do_solve(args, kwargs):
    """Read pieces from the appropriate input, solve the secret and write it to the appropriate output
    """
    kwargs['masked_secret'] = args.masked_secret

    if args.input is not None:
        pieces = tuple(
            yaml.safe_load(piece.read_text(encoding='utf-8'))
            for piece in Path(args.input).glob(args.piece_name_pattern))
    else:
        pieces = tuple(yaml.safe_load_all(io.TextIOWrapper(
            sys.stdin.buffer, encoding='utf-8').read()))

    secret = solve(pieces, **kwargs)

    output_stream = args.output if args.output is not None else sys.stdout
    if isinstance(secret, bytes):
        output_stream.buffer.write(secret)
    else:
        output_stream.write(secret)

    return 0


sys.exit(main())
