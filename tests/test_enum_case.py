"""
Regresion test for
    Enum values that differ in case get conflated #570
    https://github.com/tiangolo/typer/discussions/570
"""
from enum import Enum

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()
app = typer.Typer()


class Case(str, Enum):
    UPPER = "CASE"
    TITLE = "Case"
    LOWER = "case"

    def __str__(self) -> str:
        return self.value


@app.command()
def enum_case(case: Case):
    print(case)


@pytest.mark.parametrize("case", Case)
def test_enum_case(case: Case):
    result = runner.invoke(app, [f"{case}"])
    assert result.exit_code == 0
    assert case in result.output
