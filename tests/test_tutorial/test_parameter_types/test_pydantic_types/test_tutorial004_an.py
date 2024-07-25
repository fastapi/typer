import subprocess
import sys

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.pydantic_types import tutorial004_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_tuple():
    result = runner.invoke(app, ["--server", "Example", "::1", "https://example.com"])
    assert result.exit_code == 0
    assert "name: Example" in result.output
    assert "address: ::1" in result.output
    assert "url: https://example.com" in result.output


def test_tuple_invalid_ip():
    result = runner.invoke(
        app, ["--server", "Invalid", "invalid", "https://example.com"]
    )
    assert result.exit_code != 0
    assert "value is not a valid IPv4 or IPv6 address" in result.output


def test_tuple_invalid_url():
    result = runner.invoke(app, ["--server", "Invalid", "::1", "invalid"])
    assert result.exit_code != 0
    assert "Input should be a valid URL" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
