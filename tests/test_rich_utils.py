import importlib

import pytest
import typer
import typer.completion
from typer.rich_utils import print
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


@pytest.mark.parametrize(
    "terminal_width,stdout",
    [
        ("5", "Hello\nWorld"),
        ("20", "Hello World"),
    ],
    ids=[
        "terminal-small",
        "terminal-large",
    ],
)
def test_print(terminal_width, stdout):
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main():
        # Reloading the module as the TERMINAL_WIDTH env var is only being loaded once.
        importlib.reload(typer.rich_utils)

        print("Hello World")

    result = runner.invoke(app, env={"TERMINAL_WIDTH": terminal_width})
    assert stdout in result.stdout
