import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.enum import tutorial004 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network [simple|conv|lstm]" in result.output.replace("  ", "")


def test_main():
    result = runner.invoke(app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_invalid():
    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code != 0
    assert "Invalid value for '--network'" in result.output
    assert (
        "invalid choice: capsule. (choose from" in result.output
        or "'capsule' is not one of" in result.output
    )
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
