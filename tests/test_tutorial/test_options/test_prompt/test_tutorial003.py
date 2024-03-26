import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.options.prompt import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_prompt():
    result = runner.invoke(app, input="Old Project\nOld Project\n")
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output


def test_prompt_not_equal():
    result = runner.invoke(
        app, input="Old Project\nNew Spice\nOld Project\nOld Project\n"
    )
    assert result.exit_code == 0
    assert "Error: The two entered values do not match" in result.output
    assert "Deleting project Old Project" in result.output


def test_option():
    result = runner.invoke(app, ["--project-name", "Old Project"])
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output
    assert "Project name: " not in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--project-name" in result.output
    assert "TEXT" in result.output
    assert "[required]" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
