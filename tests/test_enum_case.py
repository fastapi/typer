"""
Regression test for
    Enum values that differ in case get conflated #570
    https://github.com/tiangolo/typer/discussions/570
"""
from enum import Enum

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()
app = typer.Typer()


class Interval(Enum):
    ONE_MINUTE = "1m"
    ONE_MONTH = "1M"


@app.command()
def enum_case(interval: Interval):
    print(interval.value)


@pytest.mark.parametrize("interval", ["1M", "1m"])
def test_enum_case(interval: str):
    result = runner.invoke(app, [interval])
    assert result.exit_code == 0
    assert interval in result.output
