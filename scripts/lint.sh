#!/usr/bin/env bash

set -e
set -x

mypy typer
ruff check typer tests docs_src scripts
ruff format typer tests docs_src scripts --check
