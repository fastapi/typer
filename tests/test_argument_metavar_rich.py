"""Test that Argument(metavar=...) displays correctly in rich help output.

Regression test for https://github.com/fastapi/typer/issues/1156

When a custom metavar is set on an Argument, the rich help panel should:
- Show the metavar as the argument name (replacing the parameter name)
- Show the type (e.g. TEXT) in the type column
- NOT show the parameter name in the name column with the metavar in the type column
"""

import typer
from typing_extensions import Annotated
from typer.testing import CliRunner


runner = CliRunner()


def test_argument_custom_metavar_shows_as_name_in_rich_help():
    """Custom metavar should replace the argument name, not the type."""
    app = typer.Typer()

    @app.command()
    def show(user: Annotated[str, typer.Argument(metavar="MY_ARG")]):
        """Show user."""
        typer.echo(f"show user: {user}")

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output

    # The usage line should show the metavar
    assert "MY_ARG" in output

    # In the Arguments panel, MY_ARG should appear as the name
    # and TEXT should appear as the type
    # Before the fix: "user      MY_ARG" (name=user, type=MY_ARG)
    # After the fix:  "MY_ARG    TEXT"   (name=MY_ARG, type=TEXT)
    assert "MY_ARG" in output
    assert "TEXT" in output

    # The parameter name 'user' should NOT appear in the help output
    # (it should be replaced by the metavar)
    lines = output.split("\n")
    argument_section = False
    for line in lines:
        if "Arguments" in line:
            argument_section = True
        elif argument_section and "─" not in line and line.strip():
            # This is an argument line in the panel
            # It should NOT contain the raw parameter name 'user'
            assert "user" not in line.lower().split(), (
                f"Parameter name 'user' should not appear in argument panel "
                f"when metavar is set. Got: {line!r}"
            )
            break


def test_argument_without_metavar_shows_default_name():
    """Without a custom metavar, argument should show name and type normally."""
    app = typer.Typer()

    @app.command()
    def show(user: Annotated[str, typer.Argument()]):
        """Show user."""
        typer.echo(f"show user: {user}")

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output

    # Should show 'user' as name and 'TEXT' as type
    assert "user" in output
    assert "TEXT" in output


def test_argument_metavar_with_int_type():
    """Custom metavar with non-string type should show correct type."""
    app = typer.Typer()

    @app.command()
    def process(count: Annotated[int, typer.Argument(metavar="NUM")]):
        """Process items."""
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    output = result.output

    assert "NUM" in output
    assert "INTEGER" in output

    # 'count' should not appear in the arguments panel
    lines = output.split("\n")
    argument_section = False
    for line in lines:
        if "Arguments" in line:
            argument_section = True
        elif argument_section and "─" not in line and line.strip():
            assert "count" not in line.lower().split(), (
                f"Parameter name 'count' should not appear when metavar is set. Got: {line!r}"
            )
            break
