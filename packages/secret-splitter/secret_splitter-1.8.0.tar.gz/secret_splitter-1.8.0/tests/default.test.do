#!/bin/sh

# usage: redo tests/name.py.test
# scans the test file if it exists for imports and runs it if any of the import dependencies change

name="${2#tests\/}"

# while ...; do ....; done < <(grep ...) crashes on dash, so explicitely make a fifo instead
trap 'rm -rf -- "$TMPDIR"' EXIT
TMPDIR="$(mktemp -d)"
mkfifo "$TMPDIR/lines"

if [ -f "../src/$name" ]; then
    [ -z "${DEBUG+x}" ] || echo "matching source src/$name" 1>&2
    redo-ifchange "../src/$name"  # required to trigger recursive dependencies if no explicit test file

    # redo if any of the source files / modules imported in the source changed
    grep -E '^from (\.|secret_splitter|src).* import' "../src/$name" | tr . / > "$TMPDIR/lines" &
    while read -r import; do
        case "$import" in
        "from src"*)
            import="${import#from src}"
            import="${import#/}"
            import="${import%% import*}"
            [ "$import.py" = "$name" ] && continue
            [ -z "${DEBUG+x}" ] || echo "source import src/$import" 1>&2
            [ -f "../src/$import.py" ] && redo-ifchange "$import.py.test"
            [ -f "../src/$import/__init__.py" ] && redo-ifchange "$import/__init__.py.test"
            ;;
        "from secret_splitter"*)
            import="${import#from secret_splitter}"
            import="${import#/}"
            import="${import%% import*}"
            [ "$import.py" = "$name" ] && continue
            [ -z "${DEBUG+x}" ] || echo "source import secret_splitter/$import" 1>&2
            [ -f "../src/secret_splitter/$import.py" ] && redo-ifchange "secret_splitter/$import.py.test"
            [ -f "../src/secret_splitter/$import/__init__.py" ] && redo-ifchange "secret_splitter/$import/__init__.py.test"
            ;;
        "from /"*)
            # relative imports
            import="${import#from /}"
            # handle the "from . import package" case
            [ -z "${import%% import*}" ] && import="${import# import }" || import="${import%% import*}"
            dir_name="$(dirname "$name")"
            while [ "${import#/}" != "$import" ]; do
                import="${import#/}"  # remove first "/"
                dir_name="$dir_name/.."
            done
            [ -z "${DEBUG+x}" ] || echo "source rel import $dir_name/$import" 1>&2
            [ "$import.py" = "$name" ] && continue
            [ -f "../src/$dir_name/$import.py" ] && redo-ifchange "$dir_name/$import.py.test"
            [ -f "../src/$dir_name/$import/__init__.py" ] && redo-ifchange "$dir_name/$import/__init__.py.test"
            ;;
        esac
    done < "$TMPDIR/lines"
else
    [ -z "${DEBUG+x}" ] || echo "no source file $(pwd)/../src/$name" 1>&2
    redo-ifcreate "../src/$name"
fi


if [ -f "$name" ]; then
    redo-ifchange "$name"
    [ -z "${DEBUG+x}" ] || echo "this file $2" 1>&2

    # redo if any of the source files / modules imported in the test changed
    grep -E '^from (src|tests).* import' "$name" | tr . / > "$TMPDIR/lines" &
    while read -r import; do
        case "$import" in
        "from tests"*)
            import="${import#from tests}"
            import="${import#/}"
            import="${import%% import*}"
            [ "$import.py" = "$name" ] && continue
            [ -z "${DEBUG+x}" ] || echo "test import tests/$import" 1>&2
            [ -f "$import.py" ] && redo-ifchange "$import.py.test"
            [ -f "$import/__init__.py" ] && redo-ifchange "$import/__init__.py.test"
            ;;
        "from src"*)
            import="${import#from src}"
            import="${import#/}"
            import="${import%% import*}"
            [ "$import.py" = "$name" ] && continue
            [ -z "${DEBUG+x}" ] || echo "test import src/$import" 1>&2
            [ -f "../src/$import.py" ] && redo-ifchange "$import.py.test"
            [ -f "../src/$import/__init__.py" ] && redo-ifchange "./$import/__init__.py.test"
            ;;
        esac
    done < "$TMPDIR/lines"

    export PYTHONPATH="$PYTHONPATH:.."
    python "$name" 1>&2
fi
