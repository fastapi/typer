import sys
from pathlib import Path
from typing import Annotated

import typer
from typer.testing import CliRunner

from .utils import needs_py310

runner = CliRunner()


def test_annotated_argument_with_default():
    app = typer.Typer()

    @app.command()
    def cmd(val: Annotated[int, typer.Argument()] = 0):
        print(f"hello {val}")

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert "hello 0" in result.output

    result = runner.invoke(app, ["42"])
    assert result.exit_code == 0, result.output
    assert "hello 42" in result.output


@needs_py310
def test_annotated_argument_in_string_type_with_default():
    app = typer.Typer()

    @app.command()
    def cmd(val: "Annotated[int, typer.Argument()]" = 0):
        print(f"hello {val}")

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert "hello 0" in result.output

    result = runner.invoke(app, ["42"])
    assert result.exit_code == 0, result.output
    assert "hello 42" in result.output


def test_annotated_argument_with_default_factory():
    app = typer.Typer()

    def make_string():
        return "I made it"

    @app.command()
    def cmd(val: Annotated[str, typer.Argument(default_factory=make_string)]):
        print(val)

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert "I made it" in result.output

    result = runner.invoke(app, ["overridden"])
    assert result.exit_code == 0, result.output
    assert "overridden" in result.output


def test_annotated_option_with_argname_doesnt_mutate_multiple_calls():
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


def test_annotated_custom_path():
    app = typer.Typer()

    class CustomPath(Path):
        # Subclassing Path was not fully supported before 3.12
        # https://docs.python.org/3.12/whatsnew/3.12.html
        if sys.version_info < (3, 12):
            _flavour = type(Path())._flavour

    @app.command()
    def custom_parser(
        my_path: Annotated[CustomPath, typer.Argument(parser=CustomPath)],
    ):
        assert isinstance(my_path, CustomPath)

    result = runner.invoke(app, "/some/quirky/path/implementation")
    assert result.exit_code == 0
