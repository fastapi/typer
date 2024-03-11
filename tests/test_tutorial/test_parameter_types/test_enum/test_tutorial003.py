import subprocess
import sys

import pytest
import typer
from typer.testing import CliRunner

from docs_src.parameter_types.enum import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_upper():
    result = runner.invoke(app, ["--network", "LSTM"])
    assert result.exit_code == 0
    assert "Training neural network of type: LSTM" in result.output


def test_lower():
    result = runner.invoke(app, ["--network", "lstm"])
    assert result.exit_code == 0
    assert "Training neural network of type: lstm" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
