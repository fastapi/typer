import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_command_aliases_positional():
    app = typer.Typer()

    @app.command("list", "ls")
    def list_items():
        print("listed")

    @app.command("remove")
    def remove_items():
        pass

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
        pass

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
        pass

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
        pass

    @app.command("remove", aliases=["rm", "delete"])
    def remove_items():
        pass

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
        pass

    @app.command("remove")
    def remove_items():
        pass

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
        pass

    @app.command("remove")
    def remove_items():
        pass

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
        pass

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "list" in result.stdout
    assert "remove" in result.stdout

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "listed" in result.stdout
