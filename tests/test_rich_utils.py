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
