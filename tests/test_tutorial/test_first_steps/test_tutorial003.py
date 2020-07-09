import subprocess

import typer
from typer.testing import CliRunner

from docs_src.first_steps import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_1():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code != 0
    assert "Error: Missing argument 'LASTNAME'" in result.output


def test_2():
    result = runner.invoke(app, ["Camila", "Gutiérrez"])
    assert result.exit_code == 0
    assert "Hello Camila Gutiérrez" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
