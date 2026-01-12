import subprocess
import sys

from typer.testing import CliRunner

from docs_src.multiple_values.arguments_with_multiple_values import (
    tutorial002_an_py39 as mod,
)

runner = CliRunner()
app = mod.app


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAMES]..." in result.output
    assert "Arguments" in result.output
    assert "[default: Harry, Hermione, Ron]" in result.output


def test_defaults():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Harry" in result.output
    assert "Hello Hermione" in result.output
    assert "Hello Ron" in result.output


def test_invalid_args():
    result = runner.invoke(app, ["Draco", "Hagrid"])
    assert result.exit_code != 0
    assert "Argument 'names' takes 3 values" in result.output


def test_valid_args():
    result = runner.invoke(app, ["Draco", "Hagrid", "Dobby"])
    assert result.exit_code == 0
    assert "Hello Draco" in result.stdout
    assert "Hello Hagrid" in result.stdout
    assert "Hello Dobby" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
