import subprocess

from typer.testing import CliRunner

from docs_src.commands.arguments import tutorial001 as mod

app = mod.app

runner = CliRunner()


def test_help_create():
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "create [OPTIONS] USERNAME" in result.output


def test_help_delete():
    result = runner.invoke(app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "delete [OPTIONS] USERNAME" in result.output


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
