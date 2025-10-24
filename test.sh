#!/bin/bash
set -euo pipefail

case "${1:-}" in
  base)
    pytest tests/test_type_conversion.py -q
    ;;
  new)
    pytest tests/test_discovery_auto.py -q
    ;;
  *)
    echo "Usage: ./test.sh {base|new}"
    exit 1
    ;;
esac
