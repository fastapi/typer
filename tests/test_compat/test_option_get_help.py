import typer.core
from typer.testing import CliRunner

from tests.assets import compat_click7_8 as mod

runner = CliRunner()


def test_hidden_option():
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Say hello" in result.output
    assert "--name" not in result.output
    assert "/lastname" in result.output
    assert "TEST_LASTNAME" in result.output
    assert "(dynamic)" in result.output


def test_hidden_option_no_rich():
    rich = typer.core.rich
    typer.core.rich = None
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "Say hello" in result.output
    assert "--name" not in result.output
    assert "/lastname" in result.output
    assert "TEST_LASTNAME" in result.output
    assert "(dynamic)" in result.output
    typer.core.rich = rich


def test_coverage_call():
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Hello John Doe, it seems you have 42" in result.output
