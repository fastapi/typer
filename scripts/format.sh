#!/bin/sh -e
set -x
set -e

ruff check typer tests docs_src scripts --fix
ruff format typer tests docs_src scripts
