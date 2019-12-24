import typer
from typer.testing import CliRunner

from first_steps.tutorial001 import main

runner = CliRunner()


def test_cli():
    app = typer.Typer()
    app.command()(main)
    result = runner.invoke(app, [])
    assert result.output == "Hello World\n"
