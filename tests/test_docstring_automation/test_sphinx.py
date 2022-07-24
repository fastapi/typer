from typing import Optional

import typer
import typer.core
from typer.testing import CliRunner


def function_to_test_sphinx_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """
    Function to test Sphinx style docstring.

    :param param1: A very detailed description.
    :type param1: str
    :param param2: A small one
    :type param2: int
    :param param3: A description with default value, defaults to None
    :type param3: Optional[str], optional
    :return: Return information.
    :rtype: str

    """


def function_to_test_priority(
    param1: str = typer.Argument(...),
    param2: int = typer.Argument(..., help="A complete different one."),
    param3: Optional[str] = None,
) -> str:
    """
    Function to test Sphinx style docstring.

    :param param1: A very detailed description, defaults to typer.Argument(...)
    :type param1: str, optional
    :param param2: A small one, defaults to typer.Argument(..., help="A complete different one.")
    :type param2: int, optional
    :param param3: A description with default value, defaults to None
    :type param3: Optional[str], optional
    :return: Return information.
    :rtype: str

    """


runner = CliRunner()


def test_sphinx_help():
    app = typer.Typer()
    app.command()(function_to_test_sphinx_docstring)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert ":param" not in result.output
    assert ":type" not in result.output
    assert ":return:" not in result.output
    assert ":rtype:" not in result.output
    assert ": str" not in result.output
    assert ": int" not in result.output
    assert "optional" not in result.output
    assert ", defaults to" not in result.output
    assert "Function to test Sphinx style docstring." in result.output
    assert "A small one." in result.output
    assert "A very detailed description." in result.output
    assert "A description with default value." in result.output


def test_help_priority():
    app = typer.Typer()
    app.command(help="Not automated!")(function_to_test_priority)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert ":param" not in result.output
    assert ":type" not in result.output
    assert ":return:" not in result.output
    assert ":rtype:" not in result.output
    assert ": str" not in result.output
    assert ": int" not in result.output
    assert "optional" not in result.output
    assert ", defaults to" not in result.output
    assert "Function to test Sphinx style docstring." not in result.output
    assert "A small one." not in result.output
    assert "Not automated!" in result.output
    assert "A very detailed description." in result.output
    assert "A complete different one." in result.output
    assert "A description with default value." in result.output
