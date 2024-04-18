import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.multiple_options import tutorial002 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "The sum is 0" in result.output


def test_1_number():
    result = runner.invoke(app, ["--number", "2"])
    assert result.exit_code == 0
    assert "The sum is 2.0" in result.output


def test_2_number():
    result = runner.invoke(app, ["--number", "2", "--number", "3", "--number", "4.5"])
    assert result.exit_code == 0
    assert "The sum is 9.5" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
