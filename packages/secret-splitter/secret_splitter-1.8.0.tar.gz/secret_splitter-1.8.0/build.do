redo-ifchange pyproject.toml

rm -rf dist/*
python -m build 1>&2
