#!/bin/sh

if [ -z "${DECOM+x}" ]; then
    redo-ifchange tests && redo-ifchange lint
else
    DECOM='' redo tests && redo lint
fi

echo "done" 1>&2
