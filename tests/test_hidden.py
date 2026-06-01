import pytest
import typer.core
from typer.testing import CliRunner

from tests.assets import hidden_commands as mod_command
from tests.assets import hidden_option as mod_option
from tests.utils import needs_rich

runner = CliRunner()


@pytest.mark.parametrize(
    "use_rich",
    [
        pytest.param(False),
        pytest.param(True, marks=needs_rich),
    ],
)
def test_hidden_option(monkeypatch: pytest.MonkeyPatch, use_rich: bool) -> None:
    monkeypatch.setattr(typer.core, "HAS_RICH", use_rich)

    result = runner.invoke(mod_option.app, ["--help"])
    assert result.exit_code == 0
    assert "Say hello" in result.output
    assert "--name" not in result.output
    assert "/lastname" in result.output
    assert "TEST_LASTNAME" in result.output
    assert "(dynamic)" in result.output


def test_coverage_call() -> None:
    result = runner.invoke(mod_option.app)
    assert result.exit_code == 0
    assert "Hello John Doe, it seems you have 42" in result.output


@pytest.mark.parametrize(
    "use_rich",
    [
        pytest.param(False),
        pytest.param(True, marks=needs_rich),
    ],
)
def test_hidden_commands(monkeypatch: pytest.MonkeyPatch, use_rich: bool) -> None:
    monkeypatch.setattr(typer.core, "HAS_RICH", use_rich)

    result = runner.invoke(mod_command.app, ["--help"])
    assert result.exit_code == 0
    assert "visible" in result.output
    assert "hidden-decorated" not in result.output
    assert "hidden-latebound" not in result.output
    assert "hidden-subgroup" not in result.output
