#!/usr/bin/env bash

set -e
set -x

mypy typer
ruff typer tests docs_src scripts
ruff format typer tests --check
