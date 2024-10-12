import os
import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.options.callback import tutorial005 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_1():
    result = runner.invoke(app, ["--name", "Camila", "--name", "Victor"])
    assert result.exit_code == 0
    assert "Validating param: name" in result.output
    assert "Hello Camila, Victor" in result.output


def test_2():
    result = runner.invoke(app, ["--name", "rick", "--name", "Victor"])
    assert result.exit_code != 0
    assert "Invalid value for '--name': Camila must be in the list" in result.output


def test_3():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "No names provided" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_completion():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL005.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial005.py --",
            "COMP_CWORD": "1",
        },
    )
    assert "--name" in result.stdout
