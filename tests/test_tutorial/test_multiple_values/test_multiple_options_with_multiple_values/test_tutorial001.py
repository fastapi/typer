import subprocess

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.multiple_options_with_multiple_values import (
    tutorial001 as mod,
)

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "No provided users" in result.output
    assert "Aborted!" in result.output


def test_1_user():
    result = runner.invoke(app, ["--users", "Camila", "Evans"])
    assert result.exit_code == 0
    assert "Processing user: Evans, Camila" in result.output


def test_3_user():
    result = runner.invoke(
        app, ["--users", "Camila", "Evans", "--users", "Rick", "Evans"]
    )
    assert result.exit_code == 0
    assert "Processing user: Evans, Camila" in result.output
    assert "Processing user: Evans, Rick" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
