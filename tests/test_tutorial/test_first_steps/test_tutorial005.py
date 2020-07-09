import subprocess

import typer
from typer.testing import CliRunner

from docs_src.first_steps import tutorial005 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Arguments:" in result.output
    assert "NAME  [required]" in result.output
    assert "--lastname TEXT" in result.output
    assert "--formal / --no-formal" in result.output


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
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
