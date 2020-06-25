from typing import Optional
from unittest import mock

import click
import pytest
import shellingham
import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()


def test_optional():
    app = typer.Typer()

    @app.command()
    async def opt(user: Optional[str] = None):
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
    async def no_type(user):
        typer.echo(f"User: {user}")

    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_install_invalid_shell():
    app = typer.Typer()

    @app.command()
    async def main():
        typer.echo("Hello World")

    with mock.patch.object(
        shellingham, "detect_shell", return_value=("xshell", "/usr/bin/xshell")
    ):
        result = runner.invoke(app, ["--install-completion"])
        assert "Shell xshell is not supported." in result.stdout
    result = runner.invoke(app)
    assert "Hello World" in result.stdout


def test_callback_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, val1, val2):
        pass  # pragma: nocover

    @app.command()
    async def main(name: str = typer.Option(..., callback=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert (
        exc_info.value.message == "Too many CLI parameter callback function parameters"
    )


def test_callback_2_untyped_parameters_sync_callback_async_cmd():
    app = typer.Typer()

    def name_callback(ctx, value):
        typer.echo(f"info name is: {ctx.info_name}")
        typer.echo(f"value is: {value}")

    @app.command()
    async def main(name: str = typer.Option(..., callback=name_callback)):
        typer.echo("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "value is: Camila" in result.stdout


def test_callback_2_untyped_parameters_async_callback_sync_cmd():
    app = typer.Typer()

    async def name_callback(ctx, value):
        typer.echo(f"info name is: {ctx.info_name}")
        typer.echo(f"value is: {value}")

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        typer.echo("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "value is: Camila" in result.stdout


def test_callback_2_untyped_parameters_async_callback_async_cmd():
    app = typer.Typer()

    async def name_callback(ctx, value):
        typer.echo(f"info name is: {ctx.info_name}")
        typer.echo(f"value is: {value}")

    @app.command()
    async def main(name: str = typer.Option(..., callback=name_callback)):
        typer.echo("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "value is: Camila" in result.stdout


# TODO: I a tired and y 'upside-down-W' key is broken...
#
# def test_callback_3_untyped_parameters():
#     app = typer.Typer()
#
#     async def name_callback(ctx, param, value):
#         typer.echo(f"info name is: {ctx.info_name}")
#         typer.echo(f"param name is: {param.name}")
#         typer.echo(f"value is: {value}")
#
#     @app.command()
#     async def main(name: str = typer.Option(..., callback=name_callback)):
#         typer.echo("Hello World")
#
#     result = runner.invoke(app, ["--name", "Camila"])
#     assert "info name is: main" in result.stdout
#     assert "param name is: name" in result.stdout
#     assert "value is: Camila" in result.stdout


def test_autocompletion_too_many_parameters_sync_cb_async_cmd():
    app = typer.Typer()

    def name_callback(ctx, args, incomplete, val2):
        pass  # pragma: nocover

    @app.command()
    async def main(name: str = typer.Option(..., autocompletion=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert exc_info.value.message == "Invalid autocompletion callback parameters: val2"


def test_autocompletion_too_many_parameters_async_cb_sync_cmd():
    app = typer.Typer()

    async def name_callback(ctx, args, incomplete, val2):
        pass  # pragma: nocover

    @app.command()
    def main(name: str = typer.Option(..., autocompletion=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert exc_info.value.message == "Invalid autocompletion callback parameters: val2"


def test_autocompletion_too_many_parameters_async_cb_async_cmd():
    app = typer.Typer()

    def name_callback(ctx, args, incomplete, val2):
        pass  # pragma: nocover

    @app.command()
    async def main(name: str = typer.Option(..., autocompletion=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert exc_info.value.message == "Invalid autocompletion callback parameters: val2"


def test_forward_references():
    app = typer.Typer()

    @app.command()
    async def main(
        arg1, arg2: int, arg3: "int", arg4: bool = False, arg5: "bool" = False
    ):
        typer.echo(f"arg1: {type(arg1)} {arg1}")
        typer.echo(f"arg2: {type(arg2)} {arg2}")
        typer.echo(f"arg3: {type(arg3)} {arg3}")
        typer.echo(f"arg4: {type(arg4)} {arg4}")
        typer.echo(f"arg5: {type(arg5)} {arg5}")

    result = runner.invoke(app, ["Hello", "2", "invalid"])
    assert (
        "Error: Invalid value for 'ARG3': invalid is not a valid integer"
        in result.stdout
    )
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )
