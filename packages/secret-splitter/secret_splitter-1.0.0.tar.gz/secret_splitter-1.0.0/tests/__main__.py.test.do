#!/bin/sh
redo-ifchange ../src/__main__.py
redo-ifchange __init__.py.test

cd ..
secret="$(echo 'test' | python3 -m src split 3 2 --stdin | python3 -m src solve)"
if [ "$secret" != "test" ]; then
    echo "FAIL stdin / stdout flow broken: -$secret-" 1>&2
    exit 1
fi

trap 'rm -rf -- "$TMPDIR"' EXIT
TMPDIR="$(mktemp -d)"

echo "test" > "$TMPDIR/secret"
python3 -m src split 3 2 -i "$TMPDIR/secret" -o "$TMPDIR/pieces" && python3 -m src solve -i "$TMPDIR/pieces" -o "$TMPDIR/solved"

recovered="$(cat "$TMPDIR/solved")"
if [ "$recovered" != "test" ]; then
    echo "FAIL folder flow broken" 1>&2
    exit 1
fi
