import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.choices import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network" in result.output
    assert "[simple|conv|lstm]" in result.output


def test_main():
    result = runner.invoke(app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_invalid():
    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Invalid value for '--network': 'capsule' is not one of" in result.output
        or "Invalid value for '--network': invalid choice: capsule. (choose from"
        in result.output
    )
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
