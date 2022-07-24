from typing import Optional

import typer
import typer.core
from typer.testing import CliRunner


def function_to_test_numpy_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """
    Function to test Numpy style docstring.

    Parameters
    ----------
    param1 : str
        A very detailed description.
    param2 : int
        A small one
    param3 : Optional[str], optional
        A description with default value, by default None

    Returns
    -------
    str
        Return information.

    """


def function_to_test_priority(
    param1: str = typer.Argument(...),
    param2: int = typer.Argument(..., help="A complete different one."),
    param3: Optional[str] = None,
) -> str:
    """
    Function to test Numpy style docstring.

    Parameters
    ----------
    param1 : str, optional
        A very detailed description, by default typer.Argument(...)
    param2 : int, optional
        A small one, by default typer.Argument(..., help="A complete different one.")
    param3 : Optional[str], optional
        A description with default value, by default None

    Returns
    -------
    str
        Return information.

    """


runner = CliRunner()


def test_numpy_help():
    app = typer.Typer()
    app.command()(function_to_test_numpy_docstring)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Parameters" not in result.output
    assert "----------" not in result.output
    assert "Returns" not in result.output
    assert "-------" not in result.output
    assert ": str" not in result.output
    assert ": int" not in result.output
    assert "optional" not in result.output
    assert ", by default" not in result.output
    assert "Function to test Numpy style docstring." in result.output
    assert "A small one." in result.output
    assert "A very detailed description." in result.output
    assert "A description with default value." in result.output


def test_help_priority():
    app = typer.Typer()
    app.command(help="Not automated!")(function_to_test_priority)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Parameters" not in result.output
    assert "----------" not in result.output
    assert "Returns" not in result.output
    assert "-------" not in result.output
    assert ": str" not in result.output
    assert ": int" not in result.output
    assert "optional" not in result.output
    assert ", by default" not in result.output
    assert "Function to test Numpy style docstring." not in result.output
    assert "A small one." not in result.output
    assert "Not automated!" in result.output
    assert "A very detailed description." in result.output
    assert "A complete different one." in result.output
    assert "A description with default value." in result.output
