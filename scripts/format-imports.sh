#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --thirdparty typer --apply typer tests docs/src
sh ./scripts/format.sh
