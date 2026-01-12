import os
import subprocess
import sys
import typing
from pathlib import Path
from typing import Annotated
from unittest import mock

import click
import pytest
import typer
import typer._completion_shared
import typer.completion
from typer.core import _split_opt
from typer.main import solve_typer_info_defaults, solve_typer_info_help
from typer.models import ParameterInfo, TyperInfo
from typer.testing import CliRunner

from .utils import requires_completion_permission

runner = CliRunner()


def test_help_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_help(TyperInfo())
    assert value is None


def test_defaults_from_info():
    # Mainly for coverage/completeness
    value = solve_typer_info_defaults(TyperInfo())
    assert value


def test_too_many_parsers():
    def custom_parser(value: str) -> int:
        return int(value)  # pragma: no cover

    class CustomClickParser(click.ParamType):
        name = "custom_parser"

        def convert(
            self,
            value: str,
            param: typing.Optional[click.Parameter],
            ctx: typing.Optional[click.Context],
        ) -> typing.Any:
            return int(value)  # pragma: no cover

    expected_error = (
        "Multiple custom type parsers provided. "
        "`parser` and `click_type` may not both be provided."
    )

    with pytest.raises(ValueError, match=expected_error):
        ParameterInfo(parser=custom_parser, click_type=CustomClickParser())


def test_valid_parser_permutations():
    def custom_parser(value: str) -> int:
        return int(value)  # pragma: no cover

    class CustomClickParser(click.ParamType):
        name = "custom_parser"

        def convert(
            self,
            value: str,
            param: typing.Optional[click.Parameter],
            ctx: typing.Optional[click.Context],
        ) -> typing.Any:
            return int(value)  # pragma: no cover

    ParameterInfo()
    ParameterInfo(parser=custom_parser)
    ParameterInfo(click_type=CustomClickParser())


@requires_completion_permission
def test_install_invalid_shell():
    app = typer.Typer()

    @app.command()
    def main():
        print("Hello World")

    with mock.patch.object(
        typer._completion_shared, "_get_shell_name", return_value="xshell"
    ):
        result = runner.invoke(app, ["--install-completion"])
        assert "Shell xshell is not supported." in result.stdout
    result = runner.invoke(app)
    assert "Hello World" in result.stdout


def test_callback_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, param, val1, val2):
        pass  # pragma: no cover

    @app.command()
    def main(name: str = typer.Option(..., callback=name_callback)):
        pass  # pragma: no cover

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


def test_callback_4_list_none():
    app = typer.Typer()

    def names_callback(ctx, param, values: typing.Optional[list[str]]):
        if values is None:
            return values
        return [value.upper() for value in values]

    @app.command()
    def main(
        names: typing.Optional[list[str]] = typer.Option(
            None, "--name", callback=names_callback
        ),
    ):
        if names is None:
            print("Hello World")
        else:
            print(f"Hello {', '.join(names)}")

    result = runner.invoke(app, ["--name", "Sideshow", "--name", "Bob"])
    assert "Hello SIDESHOW, BOB" in result.stdout

    result = runner.invoke(app, [])
    assert "Hello World" in result.stdout


def test_empty_list_default_generator():
    def empty_list() -> list[str]:
        return []

    app = typer.Typer()

    @app.command()
    def main(
        names: Annotated[list[str], typer.Option(default_factory=empty_list)],
    ):
        print(names)

    result = runner.invoke(app)
    assert "[]" in result.output


def test_completion_argument():
    file_path = Path(__file__).parent / "assets/completion_argument.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path), "E"],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_ARGUMENT.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_argument.py E",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "Emma" in result.stdout or "_files" in result.stdout
    assert "ctx: completion_argument" in result.stderr
    assert "arg is: name" in result.stderr
    assert "incomplete is: E" in result.stderr


def test_completion_untyped_parameters():
    file_path = Path(__file__).parent / "assets/completion_no_types.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_no_types.py --name Sebastian --name Ca",
        },
    )
    assert "info name is: completion_no_types.py" in result.stderr
    assert "args is: []" in result.stderr
    assert "incomplete is: Ca" in result.stderr
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout

    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_completion_untyped_parameters_different_order_correct_names():
    file_path = Path(__file__).parent / "assets/completion_no_types_order.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_COMPLETION_NO_TYPES_ORDER.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "completion_no_types_order.py --name Sebastian --name Ca",
        },
    )
    assert "info name is: completion_no_types_order.py" in result.stderr
    assert "args is: []" in result.stderr
    assert "incomplete is: Ca" in result.stderr
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout

    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_autocompletion_too_many_parameters():
    app = typer.Typer()

    def name_callback(ctx, args, incomplete, val2):
        pass  # pragma: no cover

    @app.command()
    def main(name: str = typer.Option(..., autocompletion=name_callback)):
        pass  # pragma: no cover

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

    assert "Invalid value for 'ARG3': 'invalid' is not a valid integer" in result.output
    result = runner.invoke(app, ["Hello", "2", "3", "--arg4", "--arg5"])
    assert (
        "arg1: <class 'str'> Hello\narg2: <class 'int'> 2\narg3: <class 'int'> 3\narg4: <class 'bool'> True\narg5: <class 'bool'> True\n"
        in result.stdout
    )


def test_context_settings_inheritance_single_command():
    app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})

    @app.command()
    def main(name: str):
        pass  # pragma: no cover

    result = runner.invoke(app, ["main", "-h"])
    assert "Show this message and exit." in result.stdout


def test_split_opt():
    prefix, opt = _split_opt("--verbose")
    assert prefix == "--"
    assert opt == "verbose"

    prefix, opt = _split_opt("//verbose")
    assert prefix == "//"
    assert opt == "verbose"

    prefix, opt = _split_opt("-verbose")
    assert prefix == "-"
    assert opt == "verbose"

    prefix, opt = _split_opt("verbose")
    assert prefix == ""
    assert opt == "verbose"


def test_options_metadata_typer_default():
    app = typer.Typer(options_metavar="[options]")

    @app.command()
    def c1():
        pass  # pragma: no cover

    @app.command(options_metavar="[OPTS]")
    def c2():
        pass  # pragma: no cover

    result = runner.invoke(app, ["c1", "--help"])
    assert "Usage: root c1 [options]" in result.stdout

    result = runner.invoke(app, ["c2", "--help"])
    assert "Usage: root c2 [OPTS]" in result.stdout
