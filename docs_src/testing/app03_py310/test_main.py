import typer
from typer.testing import CliRunner

from .main import main

app = typer.Typer()
app.command()(main)

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
