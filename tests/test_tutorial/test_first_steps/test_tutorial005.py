import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.first_steps import tutorial005_py39 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Arguments" in result.output
    assert "NAME" in result.output
    assert "[required]" in result.output
    assert "--lastname" in result.output
    assert "TEXT" in result.output
    assert "--formal" in result.output
    assert "--no-formal" in result.output


def test_1():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_option_lastname():
    result = runner.invoke(app, ["Camila", "--lastname", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_option_lastname_2():
    result = runner.invoke(app, ["--lastname", "Gutiérrez", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_formal_1():
    result = runner.invoke(app, ["Camila", "--lastname", "Gutiérrez", "--formal"])
    assert result.exit_code == 0
    assert "Good day Ms. Camila Gutiérrez." in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
