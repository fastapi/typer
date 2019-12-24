#!/usr/bin/env bash
# Install Flit to be able to install all
pip install flit
# Install with Flit
flit install --deps develop
# Finally, run mkdocs
mkdocs build
