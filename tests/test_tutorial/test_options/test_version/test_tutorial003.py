import os
import subprocess

import typer
from typer.testing import CliRunner

from docs_src.options.version import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_1():
    result = runner.invoke(app, ["--name", "Rick", "--version"])
    assert result.exit_code == 0
    assert "Awesome CLI Version: 0.1.0" in result.output


def test_2():
    result = runner.invoke(app, ["--name", "rick"])
    assert result.exit_code != 0
    assert "Error: Invalid value for '--name': Only Camila is allowed" in result.output


def test_3():
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


def test_completion():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL003.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial003.py --name Rick --v",
            "COMP_CWORD": "3",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "--version" in result.stdout
