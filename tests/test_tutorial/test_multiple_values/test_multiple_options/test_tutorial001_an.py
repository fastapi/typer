import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.multiple_options import tutorial001_an as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "No provided users" in result.output
    assert "raw input = None" in result.output
    assert "Aborted" in result.output


def test_1_user():
    result = runner.invoke(app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "Processing user: Camila" in result.output


def test_3_user():
    result = runner.invoke(
        app, ["--user", "Camila", "--user", "Rick", "--user", "Morty"]
    )
    assert result.exit_code == 0
    assert "Processing user: Camila" in result.output
    assert "Processing user: Rick" in result.output
    assert "Processing user: Morty" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
