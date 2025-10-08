import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_typo_suggestion_disabled_by_default():
    """Test that typo suggestions are disabled by default"""
    app = typer.Typer()

    @app.command()
    def create():
        typer.echo("Creating...")  # pragma: no cover

    @app.command()
    def delete():
        typer.echo("Deleting...")  # pragma: no cover

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" not in result.output


def test_typo_suggestion_enabled():
    """Test that typo suggestions work when enabled"""
    app = typer.Typer(suggest_commands=True)

    @app.command()
    def create():
        typer.echo("Creating...")  # pragma: no cover

    @app.command()
    def delete():
        typer.echo("Deleting...")  # pragma: no cover

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean 'create'?" in result.output


def test_typo_suggestion_multiple_matches():
    """Test that multiple suggestions are shown when there are multiple close matches"""
    app = typer.Typer(suggest_commands=True)

    @app.command()
    def create():
        typer.echo("Creating...")  # pragma: no cover

    @app.command()
    def createnew():
        typer.echo("Creating new...")  # pragma: no cover

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" in result.output
    assert "create" in result.output and "createnew" in result.output

    # Also test that the commands work correctly
    result = runner.invoke(app, ["createnew"])
    assert result.exit_code == 0
    assert "Creating new..." in result.output


def test_typo_suggestion_no_matches():
    """Test that no suggestions are shown when there are no close matches"""
    app = typer.Typer(suggest_commands=True)

    @app.command()
    def create():
        typer.echo("Creating...")  # pragma: no cover

    @app.command()
    def delete():
        typer.echo("Deleting...")  # pragma: no cover

    result = runner.invoke(app, ["xyz"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" not in result.output


def test_typo_suggestion_exact_match_works():
    """Test that exact matches still work normally"""
    app = typer.Typer(suggest_commands=True)

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


def test_typo_suggestion_disabled_explicitly():
    """Test that typo suggestions can be explicitly disabled"""
    app = typer.Typer(suggest_commands=False)

    @app.command()
    def create():
        typer.echo("Creating...")  # pragma: no cover

    @app.command()
    def delete():
        typer.echo("Deleting...")  # pragma: no cover

    result = runner.invoke(app, ["crate"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    assert "Did you mean" not in result.output


def test_typo_suggestion_multiple_similar_commands():
    """Test that multiple similar commands are suggested with quotes around each"""
    app = typer.Typer(suggest_commands=True)

    @app.command()
    def start():
        typer.echo("Starting...")

    @app.command()
    def stop():
        typer.echo("Stopping...")

    @app.command()
    def status():
        typer.echo("Status...")

    result = runner.invoke(app, ["sta"])
    assert result.exit_code != 0
    assert "No such command 'sta'" in result.output
    assert "Did you mean 'start', 'status'?" in result.output

    # Test all commands work
    result = runner.invoke(app, ["start"])
    assert result.exit_code == 0
    assert "Starting..." in result.output

    result = runner.invoke(app, ["stop"])
    assert result.exit_code == 0
    assert "Stopping..." in result.output

    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Status..." in result.output
