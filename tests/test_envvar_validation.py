import pytest
import typer
from typer.testing import CliRunner


def test_an_envvar_that_is_not_a_string_is_named_when_declared():
    with pytest.raises(TypeError, match="envvar must be a string"):
        typer.Option("a", envvar=123)


def test_an_envvar_argument_that_is_not_a_string_is_named_when_declared():
    with pytest.raises(TypeError, match="envvar must be a string"):
        typer.Argument("a", envvar=object())


def test_envvar_names_still_work():
    app = typer.Typer()

    @app.command()
    def main(name: str = typer.Option("a", envvar=["APP_NAME", "NAME"])):
        typer.echo(f"hello {name}")

    result = CliRunner().invoke(app, [], env={"APP_NAME": "env-name"})

    assert result.exit_code == 0, result.output
    assert "hello env-name" in result.output
