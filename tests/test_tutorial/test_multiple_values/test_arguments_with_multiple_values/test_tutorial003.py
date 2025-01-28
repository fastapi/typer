import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.multiple_values.arguments_with_multiple_values import tutorial003 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAMES]..." in result.output
    assert "Arguments" in result.output
    assert "[default: Harry, Hermione, Ron, hero3]" in result.output


def test_defaults():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Harry" in result.output
    assert "Hello Hermione" in result.output
    assert "Hello Ron" in result.output
    assert "Hello Wonder woman" in result.output


def test_invalid_args():
    result = runner.invoke(app, ["Draco", "Hagrid"])
    assert result.exit_code != 0
    assert "Argument 'names' takes 4 values" in result.stdout


def test_valid_args():
    result = runner.invoke(app, ["Draco", "Hagrid", "Dobby", "hero1"])
    assert result.exit_code == 0
    assert "Hello Draco" in result.stdout
    assert "Hello Hagrid" in result.stdout
    assert "Hello Dobby" in result.stdout
    assert "Hello Superman" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
