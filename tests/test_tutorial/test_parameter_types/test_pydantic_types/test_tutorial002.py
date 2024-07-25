import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic_types import tutorial002 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_url_opt():
    result = runner.invoke(app, ["--url-opt", "https://typer.tiangolo.com"])
    assert result.exit_code == 0
    assert "url_opt: https://typer.tiangolo.com" in result.output


def test_url_opt_invalid():
    result = runner.invoke(app, ["--url-opt", "invalid"])
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
