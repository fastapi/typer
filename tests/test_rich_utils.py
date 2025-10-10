import sys

import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()


def test_rich_utils_click_rewrapp():
    app = typer.Typer(rich_markup_mode="markdown")

    @app.command()
    def main():
        """
        \b
        Some text

        Some unwrapped text
        """
        print("Hello World")

    @app.command()
    def secondary():
        """
        \b
        Secondary text

        Some unwrapped text
        """
        print("Hello Secondary World")

    result = runner.invoke(app, ["--help"])
    assert "Some text" in result.stdout
    assert "Secondary text" in result.stdout
    assert "\b" not in result.stdout
    result = runner.invoke(app, ["main"])
    assert "Hello World" in result.stdout
    result = runner.invoke(app, ["secondary"])
    assert "Hello Secondary World" in result.stdout


def test_rich_help_no_commands():
    """Ensure that the help still works for a Typer instance with no commands, but with a callback."""
    app = typer.Typer(help="My cool Typer app")

    @app.callback(invoke_without_command=True, no_args_is_help=True)
    def main() -> None:
        return None  # pragma: no cover

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Show this message" in result.stdout


def test_rich_doesnt_print_None_default():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(
        name: str,
        option_1: str = typer.Option(
            "option_1_default",
        ),
        option_2: str = typer.Option(
            ...,
        ),
    ):
        print(f"Hello {name}")
        print(f"First: {option_1}")
        print(f"Second: {option_2}")

    result = runner.invoke(app, ["--help"])
    assert "Usage" in result.stdout
    assert "name" in result.stdout
    assert "option-1" in result.stdout
    assert "option-2" in result.stdout
    assert result.stdout.count("[default: None]") == 0
    result = runner.invoke(app, ["Rick", "--option-2=Morty"])
    assert "Hello Rick" in result.stdout
    assert "First: option_1_default" in result.stdout
    assert "Second: Morty" in result.stdout


def test_rich_markup_import_regression():
    # Remove rich.markup if it was imported by other tests
    if "rich" in sys.modules:
        rich_module = sys.modules["rich"]
        if hasattr(rich_module, "markup"):
            delattr(rich_module, "markup")

    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def main(bar: str):
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert "Usage" in result.stdout
    assert "BAR" in result.stdout
