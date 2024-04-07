import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.arguments.default import tutorial002_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] [NAME]" in result.output
    assert "Arguments" in result.output
    assert "[default: (dynamic)]" in result.output


def test_call_no_arg():
    greetings = ["Hello Deadpool", "Hello Rick", "Hello Morty", "Hello Hiro"]
    for _i in range(3):
        result = runner.invoke(app)
        assert result.exit_code == 0
        assert any(greet in result.output for greet in greetings)


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
