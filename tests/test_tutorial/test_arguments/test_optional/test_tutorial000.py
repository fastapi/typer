import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.arguments.optional import tutorial000_py39 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, ["World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
