import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.options.name import tutorial001_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_option_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--name" in result.output
    assert "TEXT" in result.output
    assert "--user-name" not in result.output


def test_call():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_call_no_args():
    result = runner.invoke(app, ["--name"])
    assert result.exit_code != 0
    assert "Option '--name' requires an argument" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
