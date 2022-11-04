import subprocess

import typer
from typer.testing import CliRunner

from docs_src.options.help import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_call():
    result = runner.invoke(app, ["World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output


def test_formal():
    result = runner.invoke(app, ["World", "--formal"])
    assert result.exit_code == 0
    assert "Good day Ms. World" in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--lastname" in result.output
    assert "Customization and Utils" in result.output
    assert "--formal" in result.output
    assert "--no-formal" in result.output
    assert "--debug" in result.output
    assert "--no-debug" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
