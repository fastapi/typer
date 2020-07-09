#!/usr/bin/env bash

set -e
set -x

mypy typer
black typer tests docs_src --check
isort typer tests docs_src --check-only
