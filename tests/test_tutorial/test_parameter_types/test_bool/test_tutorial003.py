import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.bool import tutorial003 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "-f" in result.output
    assert "--force" in result.output
    assert "-F" in result.output
    assert "--no-force" in result.output


def test_force():
    result = runner.invoke(app, ["-f"])
    assert result.exit_code == 0
    assert "Forcing operation" in result.output


def test_no_force():
    result = runner.invoke(app, ["-F"])
    assert result.exit_code == 0
    assert "Not forcing" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
