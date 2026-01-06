import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_default_value_in_help():
    app = typer.Typer()

    @app.command()
    def hello(name: str = "World"):
        typer.echo(f"Hello {name}")

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "World" in result.output

