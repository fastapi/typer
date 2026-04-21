import os
from enum import Enum
from pathlib import Path
from typing import Any

import pytest
import typer
from typer import _click, models
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


def test_custom_click_type():
    class BaseNumberParamType(_click.types.ParamType):
        name = "base_integer"

        def convert(
            self,
            value: Any,
            param: _click.Parameter | None,
            ctx: _click.Context | None,
        ) -> Any:
            return int(value, 0)

    app = typer.Typer()

    @app.command()
    def custom_click_type(
        hex_value: int = typer.Argument(None, click_type=BaseNumberParamType()),
    ):
        assert hex_value == 0x56

    result = runner.invoke(app, ["0x56"])
    assert result.exit_code == 0


def test_int_range_open_bound_clamp():
    app = typer.Typer()

    @app.command()
    def custom_click_type(
        value: int = typer.Argument(
            ...,
            click_type=_click.types.IntRange(min=1, min_open=True, clamp=True),
        ),
    ):
        print(value)

    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "2" in result.output


def test_bool_convert_invalid():
    app = typer.Typer()

    @app.command()
    def main(value: bool):
        print(value)  # pragma: no cover

    result = runner.invoke(app, ["maybe"])
    assert result.exit_code == 2
    assert "is not a valid boolean" in result.output
    assert "yes" in result.output
    assert "false" in result.output


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

    monkeypatch.setattr(_click.types, "_get_argv_encoding", lambda: arg_enc)
    monkeypatch.setattr(_click.types.sys, "getfilesystemencoding", lambda: system_enc)

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

        monkeypatch.setattr(models.os, "access", fake_access)

    path = tmp_path / "some_path"
    if create_file:
        path.write_text("hello")
    else:
        path.mkdir()
    result = runner.invoke(app, ["--path", str(path)])

    assert result.exit_code != 0
    assert expected_error in result.output


def test_convert_type():
    from typer._click.types import convert_type

    # str
    assert convert_type(str) is _click.types.STRING
    assert convert_type(None) is _click.types.STRING
    assert convert_type(None, default=["a"]) is _click.types.STRING

    # tuples
    tuple_type = convert_type((str, int))
    assert isinstance(tuple_type, _click.types.Tuple)
    assert [type(item) for item in tuple_type.types] == [
        type(_click.types.STRING),
        type(_click.types.INT),
    ]

    guessed_tuple = convert_type(None, default=[(1, "x")])
    assert isinstance(guessed_tuple, _click.types.Tuple)
    assert [type(item) for item in guessed_tuple.types] == [
        type(_click.types.INT),
        type(_click.types.STRING),
    ]

    # numbers
    assert convert_type(int) is _click.types.INT
    assert convert_type(float) is _click.types.FLOAT
    assert convert_type(bool) is _click.types.BOOL

    param_type = _click.types.IntRange(min=0, max=10)
    assert convert_type(param_type) is param_type

    guessed_int = convert_type(None, default=42)
    assert guessed_int is _click.types.INT

    # custom type
    class CustomType:
        pass

    guessed_unknown = convert_type(None, default=CustomType())
    assert guessed_unknown is _click.types.STRING

    func_type = convert_type(CustomType)
    assert isinstance(func_type, _click.types.FuncParamType)
    assert func_type.name == "CustomType"


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

    converted = _click.types.STRING.convert(b"\xff", None, None)
    assert converted == "ÿ"
