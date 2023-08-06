#!/bin/sh

if [ -z "${DECOM+x}" ]; then
    redo-ifchange tests && redo-ifchange lint && redo-ifchange build
else
    DECOM='' redo tests && redo lint && redo-ifchange build
fi

echo "done" 1>&2
