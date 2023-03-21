import pytest
from typer.testing import CliRunner

from tests.assets import enum_case as mod

runner = CliRunner()


@pytest.mark.parametrize("case", mod.Case)
def test_enum_case(case: mod.Case):
    """regresion test for https://github.com/tiangolo/typer/discussions/570"""
    result = runner.invoke(mod.app, [f"{case}"])
    assert result.exit_code == 0
    assert case in result.output
