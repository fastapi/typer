import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()
rounded = ["╭", "─", "┬", "╮", "│", "├", "┼", "┤", "╰", "┴", "╯"]


def test_rich_markup_mode_default():
    app = typer.Typer()

    @app.command()
    def main(arg: str):
        """Main function"""
        print("Hello World")

    assert app.rich_markup_mode == None

    result = runner.invoke(app, ["--help"])
    assert all(c not in result.stdout for c in rounded)


def test_rich_markup_mode_rich():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(arg: str):
        """Main function"""
        print("Hello World")

    assert app.rich_markup_mode == "rich"

    result = runner.invoke(app, ["--help"])
    assert any(c in result.stdout for c in rounded)
