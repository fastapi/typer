import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic_types import tutorial002_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_email_opt():
    result = runner.invoke(app, ["--email-opt", "tiangolo@gmail.com"])
    assert result.exit_code == 0
    assert "email_opt: tiangolo@gmail.com" in result.output


def test_email_opt_invalid():
    result = runner.invoke(app, ["--email-opt", "invalid"])
    assert result.exit_code != 0
    assert "value is not a valid email address" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
