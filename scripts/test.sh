#!/usr/bin/env bash

set -e
set -x

# For tests, a large terminal width
export TERMINAL_WIDTH=3000
# Force disable terminal for tests inside of pytest, takes precedence over GITHUB_ACTIONS env var
export _TYPER_FORCE_DISABLE_TERMINAL=1
# Run autocompletion install tests in the CI
export _TYPER_RUN_INSTALL_COMPLETION_TESTS=1
# It seems xdist-pytest ensures modified sys.path to import relative modules in examples keeps working
pytest --cov --cov-report=term-missing -o console_output_style=progress --showlocals --numprocesses=auto ${@}
