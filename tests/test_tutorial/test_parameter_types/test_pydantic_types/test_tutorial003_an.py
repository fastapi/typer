import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic_types import tutorial003_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_url_list():
    result = runner.invoke(
        app, ["--url", "https://example.com", "--url", "https://example.org"]
    )
    assert result.exit_code == 0
    assert "https://example.com" in result.output
    assert "https://example.org" in result.output


def test_url_invalid():
    result = runner.invoke(app, ["--url", "invalid", "--url", "https://example.org"])
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
