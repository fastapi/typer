import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_boolean_help_display():
    app = typer.Typer()

    @app.command()
    def main(debug: bool = typer.Option(False, "--debug", help="Enable debug mode")):
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "BOOL" in result.stdout
    assert "[default: False]" in result.stdout


def test_boolean_argument_help_display():
    app = typer.Typer()

    @app.command()
    def main(force: bool = typer.Argument(False, help="Force execution")):
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Arguments might show up with their name in brackets as metavar by default in Click
    # but we want to ensure the default value is shown at least.
    assert "[default: False]" in result.stdout
