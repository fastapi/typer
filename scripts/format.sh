#!/bin/sh -e
set -x
set -e

ruff typer tests docs_src scripts --fix
ruff format typer tests docs_src scripts
