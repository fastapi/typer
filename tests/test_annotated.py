from enum import Enum
from typing import Union

import typer
from typer.testing import CliRunner
from typing_extensions import Annotated

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


class TestAnnotatedOptionAcceptsOptionalValue:
    def test_enum(self):
        app = typer.Typer()

        class OptEnum(str, Enum):
            val1 = "val1"
            val2 = "val2"

        @app.command()
        def cmd(opt: Annotated[Union[bool, OptEnum], typer.Option()] = OptEnum.val1):
            if opt is False:
                print("False")
            elif opt is True:
                print("True")
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
