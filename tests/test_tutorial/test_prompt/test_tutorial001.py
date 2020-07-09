import subprocess

import typer
from typer.testing import CliRunner

from docs_src.prompt import tutorial001 as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_cli():
    result = runner.invoke(app, input="Camila\n")
    assert result.exit_code == 0
    assert "What's your name?:" in result.output
    assert "Hello Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
