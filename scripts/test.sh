#!/usr/bin/env bash

set -e
set -x

export PYTHONPATH=./docs/src
pytest --cov=typer --cov=tests --cov=docs/src --cov-report=term-missing ${@}
bash ./scripts/lint.sh
