import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_command_with_star_args():
    app = typer.Typer()

    @app.command()
    def main(*args: str, quiet: bool = False):
        """A command with *args"""
        print(f"args: {args}, quiet: {quiet}")

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "args: (), quiet: False" in result.output


def test_command_with_double_star_kwargs():
    app = typer.Typer()

    @app.command()
    def main(quiet: bool = False, **kwargs):
        """A command with **kwargs"""
        print(f"kwargs: {kwargs}, quiet: {quiet}")

    result = runner.invoke(app, ["--quiet"])
    assert result.exit_code == 0
    assert "kwargs: {}, quiet: True" in result.output


def test_callback_with_double_star_kwargs():
    app = typer.Typer()

    @app.callback()
    def main(quiet: bool = False, **kwargs):
        """A callback with **kwargs"""
        print(f"kwargs: {kwargs}, quiet: {quiet}")

    @app.command()
    def create():
        print("create")

    result = runner.invoke(app, ["--quiet", "create"])
    assert result.exit_code == 0
    assert "kwargs: {}, quiet: True" in result.output
    assert "create" in result.output
