import subprocess

import typer
import typer.core
from typer.testing import CliRunner

from docs_src.arguments.help import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] NAME" in result.output
    assert "Arguments" in result.output
    assert "NAME" in result.output
    assert "The name of the user to greet" in result.output
    assert "[required]" in result.output


def test_help_no_rich():
    rich = typer.core.rich
    typer.core.rich = None
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] NAME" in result.output
    assert "Arguments" in result.output
    assert "NAME" in result.output
    assert "The name of the user to greet" in result.output
    assert "[required]" in result.output
    typer.core.rich = rich


def test_call_arg():
    result = runner.invoke(app, ["Camila"])
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
