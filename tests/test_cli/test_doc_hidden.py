from typer.cli import get_docs_for_click
from typer.main import get_command

from tests.assets import hidden_commands as mod_command


def test_doc_skips_hidden_commands() -> None:
    command = get_command(mod_command.app)
    assert command is not None
    ctx = command.make_context("cli", [])
    docs = get_docs_for_click(obj=command, ctx=ctx)

    assert "visible" in docs
    assert "hidden-decorated" not in docs
    assert "hidden-var" not in docs
    assert "hidden-subgroup" not in docs
