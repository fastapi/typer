from __future__ import annotations

import typer
from typer.testing import CliRunner
from typing_extensions import Annotated

runner = CliRunner()


def test_annotated():
    app = typer.Typer()

    @app.command()
    def cmd(force: Annotated[bool, typer.Option("--force")] = False):
        if force:
            print("Forcing operation")
        else:
            print("Not forcing")

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert "Not forcing" in result.output

    result = runner.invoke(app, ["--force"])
    assert result.exit_code == 0, result.output
    assert "Forcing operation" in result.output
