import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_boolean_help_display() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    ) -> None:
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "BOOL" in result.stdout
    assert "[default: False]" in result.stdout


def test_boolean_help_display_show_default_false() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        debug: bool = typer.Option(False, "--debug", help="Enable debug mode", show_default=False),
    ) -> None:
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # We check that the debug line doesn't have BOOL or [default: False]
    debug_line = [line for line in result.stdout.split("\n") if "--debug" in line][0]
    assert "BOOL" not in debug_line
    assert "[default: False]" not in debug_line


def test_boolean_help_display_true_default_secondary() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        debug: bool = typer.Option(True, "--debug/--no-debug", help="Enable debug mode"),
    ) -> None:
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "BOOL" in result.stdout
    assert "[default: debug]" in result.stdout


def test_boolean_help_display_false_default_secondary() -> None:
    app = typer.Typer()

    @app.command()
    def main(
        debug: bool = typer.Option(False, "--debug/--no-debug", help="Enable debug mode"),
    ) -> None:
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "BOOL" in result.stdout
    assert "[default: no-debug]" in result.stdout


def test_boolean_argument_help_display() -> None:
    app = typer.Typer()

    @app.command()
    def main(force: bool = typer.Argument(False, help="Force execution")) -> None:
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Arguments might show up with their name in brackets as metavar by default in Click
    # but we want to ensure the default value is shown at least.
    assert "[default: False]" in result.stdout
