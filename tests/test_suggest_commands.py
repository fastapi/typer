import pytest
import typer
import typer.core
from typer.testing import CliRunner

from tests.utils import needs_rich

runner = CliRunner()


def test_typo_suggestion_enabled():
    """Test that typo suggestions work when enabled"""
    app = typer.Typer()

    @app.command()
    def create():  # pragma: no cover
        typer.echo("Creating...")

    @app.command()
    def delete():  # pragma: no cover
        typer.echo("Deleting...")

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean 'create'?" in result.output


def test_typo_suggestion_multiple_matches():
    """Test that multiple suggestions are shown when there are multiple close matches"""
    app = typer.Typer()

    @app.command()
    def create():  # pragma: no cover
        typer.echo("Creating...")

    @app.command()
    def createnew():  # pragma: no cover
        typer.echo("Creating new...")

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" in result.output
    assert "create" in result.output and "createnew" in result.output


def test_typo_suggestion_no_matches():
    """Test that no suggestions are shown when there are no close matches"""
    app = typer.Typer()

    @app.command()
    def create():  # pragma: no cover
        typer.echo("Creating...")

    @app.command()
    def delete():  # pragma: no cover
        typer.echo("Deleting...")

    result = runner.invoke(app, ["xyz"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" not in result.output


def test_typo_suggestion_exact_match_works():
    """Test that exact matches still work normally"""
    app = typer.Typer()

    @app.command()
    def create():
        typer.echo("Creating...")

    @app.command()
    def delete():
        typer.echo("Deleting...")

    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating..." in result.output

    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Deleting..." in result.output


def test_typo_suggestion_disabled():
    """Test that typo suggestions can be explicitly disabled"""
    app = typer.Typer(suggest_commands=False)

    @app.command()
    def create():  # pragma: no cover
        typer.echo("Creating...")

    @app.command()
    def delete():  # pragma: no cover
        typer.echo("Deleting...")

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" not in result.output


@pytest.mark.parametrize(
    "use_rich",
    [
        pytest.param(False),
        pytest.param(True, marks=needs_rich),
    ],
)
def test_typo_suggestion_excludes_hidden_commands(
    monkeypatch: pytest.MonkeyPatch, use_rich: bool
) -> None:
    monkeypatch.setattr(typer.core, "HAS_RICH", use_rich)
    app = typer.Typer()

    @app.command()
    def secret_agent():  # pragma: no cover
        typer.echo("Visible command")

    @app.command(hidden=True)
    def secret_admin():
        typer.echo("Hidden command")

    result = runner.invoke(app, ["secret-admi"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "'secret-agent'" in result.output
    assert "'secret-admin'" not in result.output

    result = runner.invoke(app, ["secret-admin"])
    assert result.exit_code == 0
    assert "Hidden command" in result.output
