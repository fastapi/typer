#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs/src
# Use xdist-pytest --forked to ensure modified sys.path to import relative modules in examples keeps working
pytest --cov=typer --cov=tests --cov=docs/src --cov-report=term-missing -o console_output_style=progress --forked --numprocesses=auto ${@}
bash ./scripts/lint.sh
# Include tests for files
bash ./scripts/test-files.sh
