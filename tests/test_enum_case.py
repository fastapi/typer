import pytest
from typer.testing import CliRunner

from tests.assets import enum_case as mod

runner = CliRunner()


wrong_case = pytest.mark.xfail(
    reason="Enum values that differ in case get conflated https://github.com/tiangolo/typer/discussions/570",
    strict=True,
)


@pytest.mark.parametrize(
    "case",
    (
        pytest.param(mod.Case.UPPER, marks=wrong_case),
        pytest.param(mod.Case.TITLE, marks=wrong_case),
        pytest.param(mod.Case.LOWER),
    ),
)
def test_enum_case(case: mod.Case):
    result = runner.invoke(mod.app, [f"{case}"])
    assert result.exit_code == 0
    assert case in result.output
