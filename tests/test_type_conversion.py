import os
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Literal, get_args, get_origin

import pytest
import typer
from typer import _click, param_types
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


def test_tuple_wrong_arity(monkeypatch):
    app = typer.Typer()
    monkeypatch.setenv("COLUMNS", "200")

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
    assert "invalid literal for int()" in result.output


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


def test_str_path_resolves(tmp_path: Path) -> None:
    app = typer.Typer()
    seen: list[str] = []

    @app.command()
    def main(loc: str = typer.Option(..., resolve_path=True)):
        seen.append(loc)

    file = tmp_path / "file.txt"
    file.write_text("x", encoding="utf-8")
    non_canonical = str(tmp_path / "first_dir" / "second_dir" / ".." / "file.txt")

    result = runner.invoke(app, ["--loc", non_canonical])

    assert result.exit_code == 0
    assert ".." not in seen[0]
    assert "second_dir" not in seen[0]
    assert str(tmp_path / "first_dir" / "file.txt") in seen[0]


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
    ("default", "expected_annotation"),
    [
        (42, int),
        (0.5, float),
        ("morty", str),
        (False, bool),
        ("False", str),
        ((1, "x"), tuple[int, str]),
    ],
)
def test_default_infers_param_type(
    default: Any,
    expected_annotation: Any,
) -> None:
    app = typer.Typer()
    seen: dict[str, Any] = {}

    @app.command()
    def cmd(val=default):
        seen["val"] = val

    param = next(p for p in typer.main.get_command(app).params if p.name == "val")
    assert param.runtime_param is not None
    if get_origin(expected_annotation) is tuple:
        assert get_origin(param.runtime_param.annotation) is tuple
        assert get_args(param.runtime_param.annotation) == get_args(expected_annotation)
    else:
        assert param.runtime_param.annotation is expected_annotation

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert seen["val"] == default
    if expected_annotation in (int, float, bool, str):
        assert type(seen["val"]) is expected_annotation
    elif get_origin(expected_annotation) is tuple:
        assert isinstance(seen["val"], tuple)


@pytest.mark.parametrize(
    ("parameter", "expected_metavar"),
    [
        pytest.param(Annotated[str, typer.Option(...)], "<str>"),
        pytest.param(Annotated[int, typer.Option(...)], "<int>"),
        pytest.param(Annotated[float, typer.Option(...)], "<float>"),
        pytest.param(
            Annotated[float, typer.Option(..., min=0.666, max=3.42)], "<float range>"
        ),
        pytest.param(Annotated[bytes, typer.Option(...)], "<bytes>"),
        pytest.param(Annotated[list[str], typer.Option(...)], "<list[str]>"),
        pytest.param(Annotated[tuple[str, int], typer.Option(...)], "<str,int>"),
        pytest.param(Annotated[tuple[Path, str], typer.Option(...)], "<Path,str>"),
        pytest.param(Annotated[Path, typer.Option(...)], "<path>"),
        pytest.param(Annotated[str, typer.Option(..., resolve_path=True)], "<path>"),
        pytest.param(Annotated[Path, typer.Option(..., dir_okay=False)], "<file>"),
        pytest.param(Annotated[Path, typer.Option(..., file_okay=False)], "<dir>"),
        pytest.param(Annotated[SomeEnum, typer.Option(...)], "[one|two|three]"),
        pytest.param(Annotated[SomeEnum, typer.Argument()], "{one|two|three}"),
        pytest.param(
            Annotated[SomeEnum, typer.Option(..., show_choices=False)], "[SomeEnum]"
        ),
        pytest.param(Annotated[Literal["x", "y"], typer.Option(...)], "[x|y]"),
        pytest.param(Annotated[typer.FileText, typer.Option(...)], "<FileText>"),
        pytest.param(Annotated[datetime, typer.Option(...)], "<%Y-%m-%d>"),
        pytest.param(
            Annotated[datetime, typer.Option(..., formats=["%Y-%m-%d", "%d/%m/%Y"])],
            "<%Y-%m-%d|%d/%m/%Y>",
        ),
    ],
)
def test_param_type_help_metavar(parameter: Any, expected_metavar: str) -> None:
    app = typer.Typer()

    @app.command()
    def main(value: parameter):
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert expected_metavar in result.output


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
    app = typer.Typer()

    @app.command()
    def show(name: str = typer.Option(...)):
        print(name)

    if platform_case == "windows":
        import locale

        monkeypatch.setattr(locale, "getpreferredencoding", lambda: "latin-1")
    else:
        argv_encoding = stdin_encoding or filesystem_encoding
        monkeypatch.setattr(_click._compat, "_get_argv_encoding", lambda: argv_encoding)
        monkeypatch.setattr(sys, "getfilesystemencoding", lambda: filesystem_encoding)

    result = runner.invoke(app, [], default_map={"name": b"\xff"})
    assert result.exit_code == 0
    assert "ÿ" in result.output
