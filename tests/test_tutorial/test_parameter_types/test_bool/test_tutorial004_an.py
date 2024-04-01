import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.bool import tutorial004_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "-d" in result.output
    assert "--demo" in result.output


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Running in production" in result.output


def test_demo():
    result = runner.invoke(app, ["--demo"])
    assert result.exit_code == 0
    assert "Running demo" in result.output


def test_short_demo():
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0
    assert "Running demo" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
