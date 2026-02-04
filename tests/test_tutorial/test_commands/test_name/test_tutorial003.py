from typer.testing import CliRunner

from docs_src.commands.name import tutorial003_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands" in result.output
    assert "list" in result.output or "ls" in result.output
    assert "remove" in result.output
    assert "secretlist" not in result.output


def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Listing items" in result.output


def test_ls():
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "Listing items" in result.output


def test_secretlist():
    result = runner.invoke(app, ["secretlist"])
    assert result.exit_code == 0
    assert "Listing items" in result.output


def test_remove():
    result = runner.invoke(app, ["remove"])
    assert result.exit_code == 0
    assert "Removing items" in result.output
