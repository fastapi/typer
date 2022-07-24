from typing import Optional

import typer
import typer.core
from typer.testing import CliRunner


def function_to_test_no_style_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """Function to test No style docstring."""


def function_to_test_priority(
    param1: str = typer.Argument(...),
    param2: int = typer.Argument(..., help="A complete different one."),
    param3: Optional[str] = None,
) -> str:
    """Function to test No style docstring."""


runner = CliRunner()


def test_no_style_help():
    app = typer.Typer()
    app.command()(function_to_test_no_style_docstring)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Function to test No style docstring." in result.output


def test_help_priority():
    app = typer.Typer()
    app.command(help="Not automated!")(function_to_test_priority)

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Function to test No style docstring." not in result.output
    assert "Not automated!" in result.output
    assert "A complete different one." in result.output
