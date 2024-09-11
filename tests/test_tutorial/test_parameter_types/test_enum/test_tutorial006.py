import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.enum import tutorial006 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--groceries" in result.output
    assert "[f1|f2|f3]" in result.output
    assert "default: f1, f3" in result.output


def test_call_no_arg():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Buying groceries: Eggs, Cheese" in result.output


def test_call_single_arg():
    result = runner.invoke(app, ["--groceries", "f2"])
    assert result.exit_code == 0
    assert "Buying groceries: Bacon" in result.output


def test_call_multiple_arg():
    result = runner.invoke(app, ["--groceries", "f1", "--groceries", "f2"])
    assert result.exit_code == 0
    assert "Buying groceries: Eggs, Bacon" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
