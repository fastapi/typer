from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

import click
import pytest
import typer
from typer.testing import CliRunner
from typing_extensions import Annotated

from .utils import needs_py310

runner = CliRunner()


def test_optional():
    app = typer.Typer()

    @app.command()
    def opt(user: Optional[str] = None):
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


@needs_py310
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
    def opt(number: Optional[Tuple[int, int]] = None):
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
    [List[Path], List[SomeEnum], List[str]],
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
        Tuple[str, str],
        Tuple[str, Path],
        Tuple[Path, Path],
        Tuple[str, SomeEnum],
        Tuple[SomeEnum, SomeEnum],
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
        for element, expected_type in zip(container, expected_element_types):
            assert isinstance(element, expected_type)

    result = runner.invoke(app, ["one", "two"])
    assert result.exit_code == 0


def test_custom_parse():
    app = typer.Typer()

    @app.command()
    def custom_parser(
        hex_value: int = typer.Argument(None, parser=lambda x: int(x, 0)),
    ):
        assert hex_value == 0x56

    result = runner.invoke(app, ["0x56"])
    assert result.exit_code == 0


def test_custom_click_type():
    class BaseNumberParamType(click.ParamType):
        name = "base_integer"

        def convert(
            self,
            value: Any,
            param: Optional[click.Parameter],
            ctx: Optional[click.Context],
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


class TestOptionAcceptsOptionalValue:
    def test_enum(self):
        app = typer.Typer()

        class OptEnum(str, Enum):
            val1 = "val1"
            val2 = "val2"

        @app.command()
        def cmd(opt: Annotated[Union[bool, OptEnum], typer.Option()] = OptEnum.val1):
            if opt is False:
                print("False")

            else:
                print(opt.value)

        result = runner.invoke(app)
        assert result.exit_code == 0, result.output
        assert "False" in result.output

        result = runner.invoke(app, ["--opt"])
        assert result.exit_code == 0, result.output
        assert "val1" in result.output

        result = runner.invoke(app, ["--opt", "val1"])
        assert result.exit_code == 0, result.output
        assert "val1" in result.output

        result = runner.invoke(app, ["--opt", "val2"])
        assert result.exit_code == 0, result.output
        assert "val2" in result.output

        result = runner.invoke(app, ["--opt", "val3"])
        assert result.exit_code != 0
        assert "Invalid value for '--opt': 'val3' is not one of" in result.output

        result = runner.invoke(app, ["--opt", "0"])
        assert result.exit_code == 0, result.output
        assert "False" in result.output

        result = runner.invoke(app, ["--opt", "1"])
        assert result.exit_code == 0, result.output
        assert "val1" in result.output

    def test_int(self):
        app = typer.Typer()

        @app.command()
        def cmd(opt: Annotated[Union[bool, int], typer.Option()] = 1):
            print(opt)

        result = runner.invoke(app)
        assert result.exit_code == 0, result.output
        assert "False" in result.output

        result = runner.invoke(app, ["--opt"])
        assert result.exit_code == 0, result.output
        assert "1" in result.output

        result = runner.invoke(app, ["--opt", "2"])
        assert result.exit_code == 0, result.output
        assert "2" in result.output

        result = runner.invoke(app, ["--opt", "test"])
        assert result.exit_code != 0
        assert (
            "Invalid value for '--opt': 'test' is not a valid integer" in result.output
        )

        result = runner.invoke(app, ["--opt", "true"])
        assert result.exit_code == 0, result.output
        assert "1" in result.output

        result = runner.invoke(app, ["--opt", "off"])
        assert result.exit_code == 0, result.output
        assert "False" in result.output

    def test_path(self):
        app = typer.Typer()

        @app.command()
        def cmd(opt: Annotated[Union[bool, Path], typer.Option()] = Path(".")):
            if isinstance(opt, Path):
                print((opt / "file.py").as_posix())

        result = runner.invoke(app, ["--opt"])
        assert result.exit_code == 0, result.output
        assert "file.py" in result.output

        result = runner.invoke(app, ["--opt", "/test/path/file.py"])
        assert result.exit_code == 0, result.output
        assert "/test/path/file.py" in result.output

        result = runner.invoke(app, ["--opt", "False"])
        assert result.exit_code == 0, result.output
        assert "file.py" not in result.output
