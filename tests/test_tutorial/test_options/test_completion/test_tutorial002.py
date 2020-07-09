import os
import subprocess

import typer
from typer.testing import CliRunner

from docs_src.options.autocompletion import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_completion():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial002.py --name ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Camila" in result.stdout
    assert "Carlos" in result.stdout
    assert "Sebastian" in result.stdout


def test_1():
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
