import subprocess
import sys

import typer
import typer.core
from typer.testing import CliRunner

from docs_src.terminating import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "New user created: Camila" in result.output


def test_root():
    result = runner.invoke(app, ["root"])
    assert result.exit_code == 1
    assert "The root user is reserved" in result.output
    assert "Aborted" in result.output


def test_root_no_standalone():
    # Mainly for coverage
    result = runner.invoke(app, ["root"], standalone_mode=False)
    assert result.exit_code == 1


def test_root_no_rich():
    # Mainly for coverage
    rich = typer.core.rich
    typer.core.rich = None
    result = runner.invoke(app, ["root"])
    assert result.exit_code == 1
    assert "The root user is reserved" in result.stdout
    assert "Aborted!" in result.stdout
    typer.core.rich = rich


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
