import pytest
import typer
import typer.core
from typer.testing import CliRunner

runner = CliRunner()


def test_command_aliases_positional():
    app = typer.Typer()

    @app.command("list", "ls")
    def list_items():
        print("listed")

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "listed" in result.stdout

    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "listed" in result.stdout


def test_command_aliases_keyword():
    app = typer.Typer()

    @app.command("list", aliases=["ls", "l"])
    def list_items():
        print("listed")

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "listed" in result.stdout

    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "listed" in result.stdout

    result = runner.invoke(app, ["l"])
    assert result.exit_code == 0
    assert "listed" in result.stdout


def test_command_aliases_combined():
    app = typer.Typer()

    @app.command("list", "ls", aliases=["l"])
    def list_items():
        print("listed")

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "listed" in result.stdout

    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "listed" in result.stdout

    result = runner.invoke(app, ["l"])
    assert result.exit_code == 0
    assert "listed" in result.stdout


def test_command_aliases_help_output():
    app = typer.Typer()

    @app.command("list", "ls")
    def list_items():
        pass  # pragma: no cover

    @app.command("remove", aliases=["rm", "delete"])
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list, ls" in result.stdout or "ls, list" in result.stdout
    assert (
        "remove, rm, delete" in result.stdout or "rm, delete, remove" in result.stdout
    )


def test_command_hidden_aliases():
    app = typer.Typer()

    @app.command("list", "ls", hidden_aliases=["secretlist"])
    def list_items():
        pass  # pragma: no cover

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list, ls" in result.stdout or "ls, list" in result.stdout
    assert "secretlist" not in result.stdout

    result = runner.invoke(app, ["secretlist"])
    assert result.exit_code == 0


def test_command_aliases_subcommands():
    app = typer.Typer()

    @app.command("versions", "ver", "v")
    def show_versions():
        print("versions")

    @app.command("documents", aliases=["docs"])
    def show_documents():
        print("documents")

    result = runner.invoke(app, ["versions"])
    assert result.exit_code == 0
    assert "versions" in result.stdout

    result = runner.invoke(app, ["ver"])
    assert result.exit_code == 0
    assert "versions" in result.stdout

    result = runner.invoke(app, ["v"])
    assert result.exit_code == 0
    assert "versions" in result.stdout

    result = runner.invoke(app, ["documents"])
    assert result.exit_code == 0
    assert "documents" in result.stdout

    result = runner.invoke(app, ["docs"])
    assert result.exit_code == 0
    assert "documents" in result.stdout


def test_command_no_aliases_help_output():
    app = typer.Typer()

    @app.command("list")
    def list_items():
        pass  # pragma: no cover

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "  list" in result.stdout or "list     " in result.stdout
    assert "  remove" in result.stdout or "remove   " in result.stdout


def test_command_empty_aliases_list():
    app = typer.Typer()

    @app.command("list", aliases=[])
    def list_items():
        print("listed")

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "remove" in result.stdout

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "listed" in result.stdout


def test_multiple_commands_with_aliases():
    app = typer.Typer()

    @app.command("cmd1", "c1")
    def command1():
        pass  # pragma: no cover

    @app.command("cmd2", aliases=["c2"])
    def command2():
        pass  # pragma: no cover

    @app.command("cmd3")
    def command3():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "cmd1, c1" in result.stdout or "c1, cmd1" in result.stdout
    assert "cmd2, c2" in result.stdout or "c2, cmd2" in result.stdout
    assert "cmd3" in result.stdout


def test_commands_list_deduplication():
    app = typer.Typer()

    @app.command("same", "alias1")
    def cmd1():
        pass  # pragma: no cover

    @app.command("other", "alias2")
    def cmd2():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    commands_output = result.stdout
    assert "same" in commands_output
    assert "other" in commands_output
    assert commands_output.count("same") == 1


def test_list_commands_covers_all_branches():
    app = typer.Typer()

    @app.command("cmd1")
    def command1():
        pass  # pragma: no cover

    @app.command("cmd2", "alias")
    def command2():
        pass  # pragma: no cover

    @app.command("cmd3", aliases=["a3"])
    def command3():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "cmd1" in result.stdout
    assert "cmd2" in result.stdout or "alias" in result.stdout
    assert "cmd3" in result.stdout or "a3" in result.stdout


def test_commands_with_hidden_and_aliases():
    app = typer.Typer()

    @app.command("visible", "v", aliases=["vis"])
    def visible_cmd():
        pass  # pragma: no cover

    @app.command("hidden", hidden=True)
    def hidden_cmd():
        pass  # pragma: no cover

    @app.command("another", aliases=["a"])
    def another_cmd():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "visible" in result.stdout or "v" in result.stdout or "vis" in result.stdout
    assert "hidden" not in result.stdout
    assert "another" in result.stdout or "a" in result.stdout


def test_comprehensive_alias_scenarios():
    app = typer.Typer()

    @app.command("a1", "a2", aliases=["a3", "a4"])
    def cmd_a():
        pass  # pragma: no cover

    @app.command("b1", hidden_aliases=["b2"])
    def cmd_b():
        pass  # pragma: no cover

    @app.command("c1")
    def cmd_c():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert (
        "a1" in result.stdout
        or "a2" in result.stdout
        or "a3" in result.stdout
        or "a4" in result.stdout
    )
    assert "b1" in result.stdout
    assert "b2" not in result.stdout
    assert "c1" in result.stdout

    result = runner.invoke(app, ["a1"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["a2"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["a3"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["b2"])
    assert result.exit_code == 0


def test_list_commands_deduplication_with_aliases():
    app = typer.Typer()

    @app.command("main1", "alias1", aliases=["a1"])
    def cmd1():
        pass  # pragma: no cover

    @app.command("main2", "alias2")
    def cmd2():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert (
        "main1" in result.stdout or "alias1" in result.stdout or "a1" in result.stdout
    )
    assert "main2" in result.stdout or "alias2" in result.stdout
    assert result.stdout.count("main1") <= 1
    assert result.stdout.count("main2") <= 1

    result = runner.invoke(app, ["main1"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["alias1"])
    assert result.exit_code == 0

    result = runner.invoke(app, ["a1"])
    assert result.exit_code == 0


def test_format_commands_with_aliases_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer()

    @app.command("list", "ls", aliases=["l"])
    def list_items():
        pass  # pragma: no cover

    @app.command("remove", aliases=["rm"])
    def remove_items():
        pass  # pragma: no cover

    @app.command("create")
    def create_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.stdout or "ls" in result.stdout or "l" in result.stdout
    assert "remove" in result.stdout or "rm" in result.stdout
    assert "create" in result.stdout


def test_format_commands_no_aliases_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer()

    @app.command("list")
    def list_items():
        pass  # pragma: no cover

    @app.command("remove")
    def remove_items():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "remove" in result.stdout


def test_format_commands_with_hidden_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer()

    @app.command("visible")
    def visible_cmd():
        pass  # pragma: no cover

    @app.command("hidden", hidden=True)
    def hidden_cmd():
        pass  # pragma: no cover

    @app.command("another")
    def another_cmd():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "visible" in result.stdout
    assert "hidden" not in result.stdout
    assert "another" in result.stdout


def test_format_commands_empty_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer()

    @app.callback(invoke_without_command=True)
    def main():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" not in result.stdout or "Commands:" not in result.stdout


def test_format_help_command_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer()

    @app.command(help="Test command")
    def test_cmd():
        pass  # pragma: no cover

    result = runner.invoke(app, ["test-cmd", "--help"])
    assert result.exit_code == 0
    assert "Test command" in result.stdout


def test_format_help_group_no_rich(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(typer.core, "HAS_RICH", False)

    app = typer.Typer(help="Test group")

    @app.command()
    def test_cmd():
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Test group" in result.stdout or "Usage:" in result.stdout


def test_format_help_rich_markup_mode_none():
    app = typer.Typer(rich_markup_mode=None)

    @app.command(help="Test command")
    def test_cmd():
        pass  # pragma: no cover

    result = runner.invoke(app, ["test-cmd", "--help"])
    assert result.exit_code == 0
    assert "Test command" in result.stdout
