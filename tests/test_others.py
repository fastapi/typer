from typing import Optional

import typer
from typer.main import solve_typer_info_defaults, solve_typer_info_help
from typer.models import TyperInfo
from typer.testing import CliRunner

runner = CliRunner()


def test_optional():
    app = typer.Typer()

    @app.command()
    def opt(user: Optional[str] = None):
        if user:
            typer.echo(f"User: {user}")
        else:
            typer.echo("No user")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "No user" in result.output

    result = runner.invoke(app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_no_type():
    app = typer.Typer()

    @app.command()
    def no_type(user):
        typer.echo(f"User: {user}")

    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_help_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_help(TyperInfo())
    assert value is None


def test_defaults_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_defaults(TyperInfo())
    assert value
