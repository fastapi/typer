import pytest
import typer
from typer.models import CommandInfo
from typer.testing import CliRunner


def test_a_command_registered_with_a_non_callable_is_named():
    app = typer.Typer()
    app.registered_commands.append(CommandInfo(name="bad", callback=42))

    with pytest.raises(TypeError, match="command callback must be callable"):
        CliRunner().invoke(app, [])


def test_a_group_callback_that_is_not_callable_is_named():
    app = typer.Typer(callback=42)

    @app.command()
    def hello():
        pass

    with pytest.raises(TypeError, match="`callback` must be callable"):
        CliRunner().invoke(app, [])


def test_a_callable_callback_still_builds_the_app():
    app = typer.Typer()

    @app.callback()
    def main():
        pass

    @app.command()
    def hello():
        print("hi")

    result = CliRunner().invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "hi" in result.output
