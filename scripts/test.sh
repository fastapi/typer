#!/usr/bin/env bash

set -e
set -x

bash ./scripts/test-files.sh
# Use xdist-pytest --forked to ensure modified sys.path to import relative modules in examples keeps working
pytest --cov=typer --cov=tests --cov=docs_src --cov-report=term-missing --cov-report=xml -o console_output_style=progress --forked --numprocesses=auto ${@}
