import subprocess

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.arguments_with_multiple_values import tutorial002 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)

ARGS = [
    "README.md",
    "pyproject.toml",
    "README.md",
    "pyproject.toml",
    "pyproject.toml",
    "woohoo!",
]


def test_main() -> None:
    result = runner.invoke(app, ARGS)
    assert result.exit_code == 0
    assert result.output.count("This file exists: README.md\nwoohoo!") == 1
    assert result.output.count("This file exists: pyproject.toml\nwoohoo!") == 1


def test_script() -> None:
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
