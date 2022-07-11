import os
import subprocess
from pathlib import Path
from unittest import mock

import click
import pytest
import shellingham
import typer
import typer.completion
from typer.main import solve_typer_info_defaults, solve_typer_info_help
from typer.models import TyperInfo
from typer.testing import CliRunner

runner = CliRunner()


def test_help_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_help(TyperInfo())
    assert value is None


def test_defaults_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_defaults(TyperInfo())
    assert value


def test_install_invalid_shell():
    app = typer.Typer()

    @app.command()
    def main():
        print("Hello World")

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
    def main(name: str = typer.Option(..., callback=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert (
        exc_info.value.message == "Too many CLI parameter callback function parameters"
    )


def test_callback_2_untyped_parameters():
    app = typer.Typer()

    def name_callback(ctx, value):
        print(f"info name is: {ctx.info_name}")
        print(f"value is: {value}")

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        print("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "value is: Camila" in result.stdout


def test_callback_3_untyped_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, value):
        print(f"info name is: {ctx.info_name}")
        print(f"param name is: {param.name}")
        print(f"value is: {value}")

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        print("Hello World")

    result = runner.invoke(app, ["--name", "Camila"])
    assert "info name is: main" in result.stdout
    assert "param name is: name" in result.stdout
    assert "value is: Camila" in result.stdout


def test_completion_untyped_parameters():
    file_path = Path(__file__).parent / "assets/completion_no_types.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_no_types.py --name Sebastian --name Ca",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "info name is: completion_no_types.py" in result.stderr
    # TODO: when deprecating Click 7, remove second option
    assert (
        "args is: []" in result.stderr
        or "args is: ['--name', 'Sebastian', '--name']" in result.stderr
    )
    assert "incomplete is: Ca" in result.stderr
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout

    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_completion_untyped_parameters_different_order_correct_names():
    file_path = Path(__file__).parent / "assets/completion_no_types_order.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES_ORDER.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_no_types_order.py --name Sebastian --name Ca",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "info name is: completion_no_types_order.py" in result.stderr
    # TODO: when deprecating Click 7, remove second option
    assert (
        "args is: []" in result.stderr
        or "args is: ['--name', 'Sebastian', '--name']" in result.stderr
    )
    assert "incomplete is: Ca" in result.stderr
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout

    result = subprocess.run(
        ["coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_autocompletion_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, args, incomplete, val2):
        pass  # pragma: nocover

    @app.command()
    def main(name: str = typer.Option(..., autocompletion=name_callback)):
        pass  # pragma: nocover

    with pytest.raises(click.ClickException) as exc_info:
        runner.invoke(app, ["--name", "Camila"])
    assert exc_info.value.message == "Invalid autocompletion callback parameters: val2"


def test_forward_references():
    app = typer.Typer()

    @app.command()
    def main(arg1, arg2: int, arg3: "int", arg4: bool = False, arg5: "bool" = False):
        print(f"arg1: {type(arg1)} {arg1}")
        print(f"arg2: {type(arg2)} {arg2}")
        print(f"arg3: {type(arg3)} {arg3}")
        print(f"arg4: {type(arg4)} {arg4}")
        print(f"arg5: {type(arg5)} {arg5}")

    result = runner.invoke(app, ["Hello", "2", "invalid"])
    # TODO: when deprecating Click 7, remove second option

    assert (
        "Invalid value for 'ARG3': 'invalid' is not a valid integer" in result.stdout
        or "Invalid value for 'ARG3': invalid is not a valid integer" in result.stdout
    )
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )


def test_context_settings_inheritance_single_command():
    app = typer.Typer(context_settings=dict(help_option_names=["-h", "--help"]))

    @app.command()
    def main(name: str):
        pass  # pragma: nocover

    result = runner.invoke(app, ["main", "-h"])
    assert "Show this message and exit." in result.stdout
