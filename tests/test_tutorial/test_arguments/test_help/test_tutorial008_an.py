import subprocess
import sys

import pytest
import typer
import typer.core
from typer.testing import CliRunner

from docs_src.arguments.help import tutorial008_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Say hi to NAME very gently, like Dirk." in result.output
    assert "Arguments" not in result.output
    assert "[default: World]" not in result.output


def test_help_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Say hi to NAME very gently, like Dirk." in result.output
    assert "Arguments" not in result.output
    assert "[default: World]" not in result.output


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
