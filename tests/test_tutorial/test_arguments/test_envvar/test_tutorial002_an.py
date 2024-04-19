import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.arguments.envvar import tutorial002_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Arguments" in result.output
    assert "env var: AWESOME_NAME, GOD_NAME" in result.output
    assert "default: World" in result.output


def test_call_arg():
    result = runner.invoke(app, ["Wednesday"])
    assert result.exit_code == 0
    assert "Hello Mr. Wednesday" in result.output


def test_call_env_var1():
    result = runner.invoke(app, env={"AWESOME_NAME": "Wednesday"})
    assert result.exit_code == 0
    assert "Hello Mr. Wednesday" in result.output


def test_call_env_var2():
    result = runner.invoke(app, env={"GOD_NAME": "Anubis"})
    assert result.exit_code == 0
    assert "Hello Mr. Anubis" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
