#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place docs_src typer tests --exclude=__init__.py
black typer tests docs_src
isort typer tests docs_src
