import subprocess

import typer
from typer.testing import CliRunner

from docs_src.terminating import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User created: Camila" in result.output
    assert "Notification sent for new user: Camila" in result.output


def test_existing():
    result = runner.invoke(app, ["rick"])
    assert result.exit_code == 0
    assert "The user already exists" in result.output
    assert "Notification sent for new user" not in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
