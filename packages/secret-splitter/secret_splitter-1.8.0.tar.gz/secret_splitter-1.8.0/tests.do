#!/bin/sh

redo-ifchange tests/secret_splitter/__init__.py.test
redo-ifchange tests/secret_splitter/__main__.py.test

[ -z "${DECOM+x}" ] || (
    find tests/decommissioned -name "*.py" | \
        awk -e '{ print $0".test" }' | xargs -n 1 redo-ifchange
)
