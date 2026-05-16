"""Tests for `typer ... utils docs` Markdown output respecting hidden parameters/commands.

`utils docs` walks the Click command tree and must stay consistent with the interactive
`--help` text (Rich): anything marked `hidden=True` should not appear in generated docs.
"""

import click
import typer
from typer.cli import get_docs_for_click
from typer.main import get_command


def test_get_docs_for_click_omits_hidden_subcommands() -> None:
    """Hidden subcommands must not appear in the command list or get nested sections."""

    app = typer.Typer()

    @app.command()
    def public_cmd() -> None:
        """Visible to users."""
        pass

    @app.command(hidden=True)
    def secret_cmd() -> None:
        """Internal helper; should not be exported to Markdown."""
        pass

    click_obj = get_command(app)
    with click.Context(click_obj, info_name="demo") as ctx:
        md = get_docs_for_click(obj=click_obj, ctx=ctx, name="demo")

    # Typer/Click expose CLI names with hyphens by default.
    assert "`public-cmd`" in md
    assert "secret-cmd" not in md


def test_get_docs_for_click_omits_hidden_options() -> None:
    """Hidden options should not appear under **Options** in generated Markdown."""

    app = typer.Typer()

    @app.command()
    def main(
        visible: str = typer.Option("", "--visible", help="Shown."),
        _legacy: str = typer.Option("", "--legacy", hidden=True, help="Deprecated."),
    ) -> None:
        pass

    click_obj = get_command(app)
    with click.Context(click_obj, info_name="demo") as ctx:
        md = get_docs_for_click(obj=click_obj, ctx=ctx, name="demo")

    assert "--visible" in md
    assert "--legacy" not in md
