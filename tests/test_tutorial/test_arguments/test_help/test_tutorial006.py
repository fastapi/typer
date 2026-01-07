import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.arguments.help import tutorial006_py39 as mod

runner = CliRunner()

app = typer.Typer(rich_markup_mode=None)
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] ✨user✨" in result.output
    assert "Arguments" in result.output
    assert "✨user✨" in result.output
    assert "name" not in result.output
    assert "[default: World]" in result.output


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
