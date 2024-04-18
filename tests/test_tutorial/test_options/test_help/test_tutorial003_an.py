import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.options.help import tutorial003_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_call():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello Wade Wilson" in result.output


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--fullname" in result.output
    assert "TEXT" in result.output
    assert "[default: Wade Wilson]" not in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
