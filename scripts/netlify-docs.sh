#!/usr/bin/env bash
# Install Flit to be able to install all
python3 -m pip install flit
# Install with Flit
python3 -m flit install --deps develop
# Finally, run mkdocs
python3 -m mkdocs build
