#!/bin/sh

if [ -z "${DECOM+x}" ]; then
    find src/ \! -wholename "*decommissioned*" -and -name "*.py" | \
        awk -e '{ print $0".lint" }' | xargs -n 1 redo-ifchange
    find tests/ \! -wholename "*decommissioned*" -and -name "*.py" | \
        awk -e '{ print $0".lint" }' | xargs -n 1 redo-ifchange
else
    find src/ -name "*.py" | \
        awk -e '{ print $0".lint" }' | xargs -n 1 redo-ifchange
    find tests/ -name "*.py" | \
        awk -e '{ print $0".lint" }' | xargs -n 1 redo-ifchange
fi
