import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.number import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Verbose level is 0" in result.output


def test_verbose_1():
    result = runner.invoke(app, ["--verbose"])
    assert result.exit_code == 0
    assert "Verbose level is 1" in result.output


def test_verbose_3():
    result = runner.invoke(app, ["--verbose", "--verbose", "--verbose"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_verbose_short_1():
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert "Verbose level is 1" in result.output


def test_verbose_short_3():
    result = runner.invoke(app, ["-v", "-v", "-v"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_verbose_short_3_condensed():
    result = runner.invoke(app, ["-vvv"])
    assert result.exit_code == 0
    assert "Verbose level is 3" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
