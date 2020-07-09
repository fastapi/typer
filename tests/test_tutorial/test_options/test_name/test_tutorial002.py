import subprocess

import typer
from typer.testing import CliRunner

from docs_src.options.name import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_option_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "-n, --name TEXT" in result.output
    assert "--user-name" not in result.output


def test_call():
    result = runner.invoke(app, ["-n", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_call_long():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
