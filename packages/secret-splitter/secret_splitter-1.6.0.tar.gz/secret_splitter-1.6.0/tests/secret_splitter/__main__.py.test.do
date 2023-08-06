#!/bin/sh
redo-ifchange ../../src/secret_splitter/__main__.py
redo-ifchange __init__.py.test

cd ../../src
secret="$(echo 'test' | python -m secret_splitter split 3 2 --stdin | python -m secret_splitter solve)"
if [ "$secret" != "test" ]; then
    echo "FAIL stdin / stdout flow broken: -$secret-" 1>&2
    exit 1
fi

trap 'rm -rf -- "$TMPDIR"' EXIT
TMPDIR="$(mktemp -d)"

echo "test" > "$TMPDIR/secret"
python -m secret_splitter split 3 2 -i "$TMPDIR/secret" -o "$TMPDIR/pieces" && python -m secret_splitter solve -i "$TMPDIR/pieces" -o "$TMPDIR/solved"

recovered="$(cat "$TMPDIR/solved")"
if [ "$recovered" != "test" ]; then
    echo "FAIL folder flow broken" 1>&2
    exit 1
fi
