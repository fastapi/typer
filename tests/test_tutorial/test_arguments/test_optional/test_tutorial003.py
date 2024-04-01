import subprocess
import sys

import typer
import typer.core
from typer.testing import CliRunner

from docs_src.arguments.optional import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_call_no_arg():
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "Missing argument 'NAME'." in result.output


def test_call_no_arg_standalone():
    # Mainly for coverage
    result = runner.invoke(app, standalone_mode=False)
    assert result.exit_code != 0


def test_call_no_arg_no_rich():
    # Mainly for coverage
    rich = typer.core.rich
    typer.core.rich = None
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "Error: Missing argument 'NAME'" in result.stdout
    typer.core.rich = rich


def test_call_arg():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
