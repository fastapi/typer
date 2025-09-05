import subprocess

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.enum import tutorial004 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_enum_names_default():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Log level set to: WARNING" in result.output


def test_enum_names():
    result = runner.invoke(app, ["--log-level", "debug"])
    assert result.exit_code == 0
    assert "Log level set to: DEBUG" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
