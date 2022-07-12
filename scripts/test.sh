#!/usr/bin/env bash

set -e
set -x

# For tests, a large terminal width
export TERMINAL_WIDTH=3000
# Force disable terminal for tests inside of pytest, takes precedence over GITHUB_ACTIONS env var
export _TYPER_FORCE_DISABLE_TERMINAL=1
bash ./scripts/test-files.sh
# Use xdist-pytest --forked to ensure modified sys.path to import relative modules in examples keeps working
pytest --cov=typer --cov=tests --cov=docs_src --cov-report=term-missing --cov-report=xml -o console_output_style=progress --forked --numprocesses=auto ${@}
