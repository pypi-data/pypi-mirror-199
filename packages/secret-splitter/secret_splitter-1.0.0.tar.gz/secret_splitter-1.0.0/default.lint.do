#!/bin/sh

redo-ifchange "$2"

export PYTHONPATH="$PYTHONPATH:."
python3 -m pylint "$2" --score n 1>&2 || redo-always # don't crash but redo until fixed
