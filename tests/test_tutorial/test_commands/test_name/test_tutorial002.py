from typer.testing import CliRunner

from docs_src.commands.name import tutorial002_py310 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "list" in result.output or "ls" in result.output
    assert (
        "remove" in result.output or "rm" in result.output or "delete" in result.output
    )


def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Listing items" in result.output


def test_ls():
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "Listing items" in result.output


def test_remove():
    result = runner.invoke(app, ["remove"])
    assert result.exit_code == 0
    assert "Removing items" in result.output


def test_rm():
    result = runner.invoke(app, ["rm"])
    assert result.exit_code == 0
    assert "Removing items" in result.output


def test_delete():
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Removing items" in result.output
