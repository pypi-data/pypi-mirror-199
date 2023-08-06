#!/bin/sh

# usage: redo tests/name.py.test
# scans the test file if it exists for imports and runs it if any of the import dependencies change

name="${2#tests\/}"

trap 'rm -rf -- "$TMPDIR"' EXIT
TMPDIR="$(mktemp -d)"
mkfifo "$TMPDIR/lines"

if [ -f "../src/$name" ]; then
    [ -z "${DEBUG+x}" ] || echo "matching source src/$name" 1>&2
    redo-ifchange "../src/$name"  # required to trigger recursive dependencies if no explicit test file

    # redo if any of the source files / modules imported in the source changed
    # absolute imports
    grep '^from src.* import' "../src/$name" > "$TMPDIR/lines" &
    while read -r import; do
        # isolate package
        import="${import#from src}"
        import="${import#.}"
        import="${import%% import*}"
        #import="${import//./\/}"  # turn modules in folders
        import="$(printf '%s\n' "$import" | tr . /)"
        [ "$import.py" = "$name" ] && continue
        [ -z "${DEBUG+x}" ] || echo "source import src/$import" 1>&2
        [ -f "../src/$import.py" ] && redo-ifchange "$import.py.test"
        [ -f "../src/$import/__init__.py" ] && redo-ifchange "$import/__init__.py.test"
    done < "$TMPDIR/lines"

    # relative imports
    grep '^from \..* import' "../src/$name" > "$TMPDIR/lines" &
    while read -r import; do
        # isolate package
        import="${import#from }"
        import="${import#.}"
        # handle the "from . import package" case
        [ -z "${import%% import*}" ] && import="${import# import }" || import="${import%% import*}"
        dir_name="$(dirname "$name")"
        while [ "${import#.}" != "$import" ]; do
            import="${import#.}"  # remove first "."
            dir_name="$dir_name/.."
        done
        #import="${import//./\/}"  # turn modules in folders
        import="$(printf '%s\n' "$import" | tr . /)"
        [ -z "${DEBUG+x}" ] || echo "source rel import $dir_name/$import" 1>&2
        [ "$import.py" = "$name" ] && continue
        [ -f "../src/$dir_name/$import.py" ] && redo-ifchange "$dir_name/$import.py.test"
        [ -f "../src/$dir_name/$import/__init__.py" ] && redo-ifchange "$dir_name/$import/__init__.py.test"
    done < "$TMPDIR/lines"
else
    [ -z "${DEBUG+x}" ] || echo "no source file $(pwd)/../src/$name" 1>&2
    redo-ifcreate "../src/$name"
fi


if [ -f "$name" ]; then
    redo-ifchange "$name"
    [ -z "${DEBUG+x}" ] || echo "this file $2" 1>&2

    # redo if any of the source files / modules imported in the test changed
    grep '^from tests.* import' "$name" > "$TMPDIR/lines" &
    while read -r import; do
        # isolate package
        import="${import#from tests}"
        import="${import#.}"
        import="${import%% import*}"
        #import="${import//./\/}"  # turn modules in folders
        import="$(printf '%s\n' "$import" | tr . /)"
        [ "$import.py" = "$name" ] && continue
        [ -z "${DEBUG+x}" ] || echo "test import tests/$import" 1>&2
        [ -f "$import.py" ] && redo-ifchange "$import.py.test"
        [ -f "$import/__init__.py" ] && redo-ifchange "$import/__init__.py.test"
    done < "$TMPDIR/lines"

    grep '^from src.* import' "$name" > "$TMPDIR/lines" &
    while read -r import; do
        # isolate package
        import="${import#from src}"
        import="${import#.}"
        import="${import%% import*}"
        #import="${import//./\/}"  # turn modules in folders
        import="$(printf '%s\n' "$import" | tr . /)"
        [ "$import.py" = "$name" ] && continue
        [ -z "${DEBUG+x}" ] || echo "test import src/$import" 1>&2
        [ -f "../src/$import.py" ] && redo-ifchange "$import.py.test"
        [ -f "../src/$import/__init__.py" ] && redo-ifchange "./$import/__init__.py.test"
    done < "$TMPDIR/lines"

    export PYTHONPATH="$PYTHONPATH:.."
    python3 "$name" 1>&2
fi
