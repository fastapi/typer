import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any

import pytest
import typer
from typer import _click, param_types
from typer.param_types import (
    BOOL,
    FLOAT,
    INT,
    STRING,
    FuncParamType,
    TyperPath,
    resolve_param_type,
)
from typer.testing import CliRunner

from tests.utils import needs_linux, needs_windows

runner = CliRunner()


def test_optional():
    app = typer.Typer()

    @app.command()
    def opt(user: str | None = None):
        if user:
            print(f"User: {user}")
        else:
            print("No user")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "No user" in result.output

    result = runner.invoke(app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_union_type_optional():
    app = typer.Typer()

    @app.command()
    def opt(user: str | None = None):
        if user:
            print(f"User: {user}")
        else:
            print("No user")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "No user" in result.output

    result = runner.invoke(app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


def test_optional_tuple():
    app = typer.Typer()

    @app.command()
    def opt(number: tuple[int, int] | None = None):
        if number:
            print(f"Number: {number}")
        else:
            print("No number")

    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "No number" in result.output

    result = runner.invoke(app, ["--number", "4", "2"])
    assert result.exit_code == 0
    assert "Number: (4, 2)" in result.output


def test_no_type():
    app = typer.Typer()

    @app.command()
    def no_type(user):
        print(f"User: {user}")

    result = runner.invoke(app, ["Camila"])
    assert result.exit_code == 0
    assert "User: Camila" in result.output


class SomeEnum(Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"


@pytest.mark.parametrize(
    "type_annotation",
    [list[Path], list[SomeEnum], list[str]],
)
def test_list_parameters_convert_to_lists(type_annotation):
    # Lists containing objects that are converted by Click (i.e. not Path or Enum)
    # should not be inadvertently converted to tuples
    expected_element_type = type_annotation.__args__[0]
    app = typer.Typer()

    @app.command()
    def list_conversion(container: type_annotation):
        assert isinstance(container, list)
        for element in container:
            assert isinstance(element, expected_element_type)

    result = runner.invoke(app, ["one", "two", "three"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "type_annotation",
    [
        tuple[str, str],
        tuple[str, Path],
        tuple[Path, Path],
        tuple[str, SomeEnum],
        tuple[SomeEnum, SomeEnum],
    ],
)
def test_tuple_parameter_elements_are_converted_recursively(type_annotation):
    # Tuple elements that aren't converted by Click (i.e. Path or Enum)
    # should be recursively converted by Typer
    expected_element_types = type_annotation.__args__
    app = typer.Typer()

    @app.command()
    def tuple_recursive_conversion(container: type_annotation):
        assert isinstance(container, tuple)
        for element, expected_type in zip(
            container, expected_element_types, strict=True
        ):
            assert isinstance(element, expected_type)

    result = runner.invoke(app, ["one", "two"])
    assert result.exit_code == 0


def test_tuple_wrong_arity():
    app = typer.Typer()

    @app.command()
    def tuple_arity(value: tuple[str, str] = typer.Option(...)):
        print(value)  # pragma: no cover

    result = runner.invoke(app, [], default_map={"value": ("only-one",)})
    assert result.exit_code == 2
    assert "2 values are required, but 1 given." in result.output


def test_custom_parse():
    app = typer.Typer()

    @app.command()
    def custom_parser(
        hex_value: int = typer.Argument(None, parser=lambda x: int(x, 0)),
    ):
        assert hex_value == 0x56

    result = runner.invoke(app, ["0x56"])
    assert result.exit_code == 0


def test_custom_parse_value_error():
    app = typer.Typer()

    @app.command()
    def custom_parser(
        hex_value: int = typer.Argument(None, parser=lambda x: int(x, 0)),
    ):
        print(hex_value)  # pragma: no cover

    result = runner.invoke(app, ["not-a-hex"])
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_custom_parser_hex():
    app = typer.Typer()

    @app.command()
    def custom_parser_hex(
        hex_value: int = typer.Argument(None, parser=lambda x: int(x, 0)),
    ):
        assert hex_value == 0x56

    result = runner.invoke(app, ["0x56"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    ("cli_value", "expected"),
    [
        ("true", True),
        ("false", False),
        ("yes", True),
        ("no", False),
        ("1", True),
        ("0", False),
        ("on", True),
        ("off", False),
        ("t", True),
        ("f", False),
        ("y", True),
        ("n", False),
        ("", False),
        (" true ", True),
        (" FALSE ", False),
        ("TRUE", True),
        ("No", False),
    ],
)
def test_bool_convert_valid(cli_value: str, expected: bool) -> None:
    app = typer.Typer()

    @app.command()
    def main(value: bool):
        print(value)

    result = runner.invoke(app, [cli_value])
    assert result.exit_code == 0
    assert str(expected) in result.output


def test_bool_convert_invalid():
    app = typer.Typer()

    @app.command()
    def main(value: bool):
        print(value)  # pragma: no cover

    result = runner.invoke(app, ["maybe"])
    assert result.exit_code == 2
    assert "Input should be a valid boolean" in result.output


@pytest.mark.parametrize(
    ("arg_enc", "system_enc", "raw_value", "expected_output"),
    [
        pytest.param("latin-1", "utf-8", b"\xff", "ÿ"),
        pytest.param("ascii", "latin-1", b"\xff", "ÿ"),
        pytest.param("ascii", "utf-16", b"\xff", "�"),
        pytest.param("ascii", "ascii", b"\xff", "�"),
    ],
)
def test_string_param_type_converts_bytes(
    monkeypatch: pytest.MonkeyPatch,
    arg_enc: str,
    system_enc: str,
    raw_value: bytes,
    expected_output: str,
):
    app = typer.Typer()

    @app.command()
    def show(name: str = typer.Option(...)):
        print(name)

    command = typer.main.get_command(app)
    name_param = next(param for param in command.params if param.name == "name")
    assert repr(name_param.type) == "STRING"

    monkeypatch.setattr(_click._compat, "_get_argv_encoding", lambda: arg_enc)
    monkeypatch.setattr(sys, "getfilesystemencoding", lambda: system_enc)

    result = runner.invoke(app, [], default_map={"name": raw_value})
    assert result.exit_code == 0
    assert expected_output in result.output


@pytest.mark.parametrize("path_type", [str, bytes, Path])
def test_path_coerced(path_type) -> None:
    # Ensure coerce_path_result works correctly
    app = typer.Typer()

    @app.command()
    def show(path: Any = typer.Option(..., path_type=path_type)):
        print(path)

    result = runner.invoke(app, ["--path", "dir/my_awesome_file.txt"])
    assert result.exit_code == 0
    assert "my_awesome_file" in result.output


def test_str_with_path_options() -> None:
    app = typer.Typer()

    @app.command()
    def warp(loc: str = typer.Option(..., resolve_path=True)):
        print(loc)

    param = next(p for p in typer.main.get_command(app).params if p.name == "loc")
    assert isinstance(param.type, TyperPath)


@pytest.mark.parametrize(
    ("create_file", "option_kwargs", "deny_mode", "expected_error"),
    [
        (True, {"file_okay": False, "dir_okay": True}, None, "is a file"),
        (False, {"file_okay": True, "dir_okay": False}, None, "is a directory"),
        (True, {"readable": True}, os.R_OK, "is not readable"),
        (True, {"readable": False, "writable": True}, os.W_OK, "is not writable"),
    ],
)
def test_path_convert_failures(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    create_file: bool,
    option_kwargs: dict[str, bool],
    deny_mode: int | None,
    expected_error: str,
) -> None:
    app = typer.Typer()

    @app.command()
    def show(path: Path = typer.Option(..., **option_kwargs)):
        print(path)  # pragma: no cover

    if deny_mode is not None:
        original_access = os.access

        def fake_access(path: str, mode: int) -> bool:
            if mode == deny_mode:
                return False
            return original_access(path, mode)  # pragma: no cover

        monkeypatch.setattr(param_types.os, "access", fake_access)

    path = tmp_path / "some_path"
    if create_file:
        path.write_text("hello")
    else:
        path.mkdir()
    result = runner.invoke(app, ["--path", str(path)])

    assert result.exit_code != 0
    assert expected_error in result.output


@pytest.mark.parametrize(
    ("default", "expected_param_type", "expected_value", "value_type"),
    [
        (42, INT, 42, int),
        (0.5, FLOAT, 0.5, float),
        ("morty", STRING, "morty", str),
        (False, BOOL, False, bool),
        ("False", STRING, "False", str),
    ],
)
def test_default_infers_param_type(
    default: Any,
    expected_param_type: Any,
    expected_value: Any,
    value_type: type,
) -> None:
    app = typer.Typer()
    seen: dict[str, Any] = {}

    @app.command()
    def cmd(val=default):
        seen["val"] = val

    param = next(p for p in typer.main.get_command(app).params if p.name == "val")
    assert param.type is expected_param_type

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert seen["val"] == expected_value
    assert type(seen["val"]) is value_type


def test_convert_type():
    # str
    assert resolve_param_type(str) is STRING
    assert resolve_param_type(None) is STRING
    assert resolve_param_type(None, default=["a"]) is STRING

    # tuples
    tuple_type = resolve_param_type((str, int))
    assert isinstance(tuple_type, _click.types.Tuple)
    assert [type(item) for item in tuple_type.types] == [type(STRING), type(INT)]

    guessed_tuple = resolve_param_type(None, default=[(1, "x")])
    assert isinstance(guessed_tuple, _click.types.Tuple)
    assert [type(item) for item in guessed_tuple.types] == [
        type(INT),
        type(STRING),
    ]

    # numbers
    assert resolve_param_type(int) is INT
    assert resolve_param_type(float) is FLOAT
    assert resolve_param_type(bool) is BOOL

    guessed_int = resolve_param_type(None, default=42)
    assert guessed_int is INT

    # custom type
    class CustomType:
        pass

    guessed_unknown = resolve_param_type(None, default=CustomType())
    assert guessed_unknown is STRING

    func_type = resolve_param_type(CustomType)
    assert isinstance(func_type, FuncParamType)
    assert func_type.name == "CustomType"


def test_int_rejects_float_default() -> None:
    app = typer.Typer()

    @app.command()
    def main(age: int = typer.Option(15.3)):
        typer.echo(age)

    result = runner.invoke(app, ["--age", 42])
    assert "42" in result.stdout

    # Pydantic validation rejects floats as int instead of converting int(15.3) to 15
    result = runner.invoke(app)
    assert result.exit_code != 0
    assert "Input should be a valid integer" in result.stderr


@pytest.mark.parametrize(
    ("platform_case", "stdin_encoding", "filesystem_encoding"),
    [
        pytest.param("windows", None, "utf-8", marks=needs_windows),
        pytest.param("linux", "latin-1", "utf-8", marks=needs_linux),
        pytest.param("linux", None, "latin-1", marks=needs_linux),
    ],
)
def test_argv_encoding(
    monkeypatch: pytest.MonkeyPatch,
    platform_case: str,
    stdin_encoding: str | None,
    filesystem_encoding: str,
) -> None:
    sys = _click._compat.sys
    if platform_case == "windows":
        import locale

        monkeypatch.setattr(locale, "getpreferredencoding", lambda: "latin-1")
    else:

        class FakeStdin:
            def __init__(self, encoding: str | None) -> None:
                self.encoding = encoding

        monkeypatch.setattr(sys, "stdin", FakeStdin(stdin_encoding))
        monkeypatch.setattr(sys, "getfilesystemencoding", lambda: filesystem_encoding)

    converted = STRING.convert(b"\xff", None, None)
    assert converted == "ÿ"
