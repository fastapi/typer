import click
import pytest

from typer.completion import shell_complete


class _FakeCompletion:
    def __init__(self, cli, ctx_args, prog_name, complete_var):
        self.cli = cli
        self.ctx_args = ctx_args
        self.prog_name = prog_name
        self.complete_var = complete_var

    def source(self):
        # This will be overridden per-test via monkeypatch on the class
        return ""

    def complete(self):
        # This will be overridden per-test via monkeypatch on the class
        return ""


@pytest.mark.parametrize(
    "instruction",
    ["complete_zsh", "source_zsh"],
)
@pytest.mark.parametrize(
    "exc",
    [click.exceptions.Abort, click.exceptions.Exit],
)
def test_shell_complete_handles_abort_and_exit(monkeypatch, capsys, instruction, exc):
    # Make Click return our fake completion class
    monkeypatch.setattr(
        click.shell_completion,
        "get_completion_class",
        lambda shell: _FakeCompletion,
    )

    # Patch the specific method used by the instruction to raise
    if instruction.startswith("complete"):
        monkeypatch.setattr(_FakeCompletion, "complete", lambda self: (_ for _ in ()).throw(exc()))
    else:
        monkeypatch.setattr(_FakeCompletion, "source", lambda self: (_ for _ in ()).throw(exc()))

    cli = click.Command("demo")

    # Should not raise, should just exit 0 with no output
    code = shell_complete(
        cli=cli,
        ctx_args={},
        prog_name="demo",
        complete_var="_DEMO_COMPLETE",
        instruction=instruction,
    )

    out = capsys.readouterr()
    assert code == 0
    assert out.out == ""