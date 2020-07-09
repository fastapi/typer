import subprocess

from typer.testing import CliRunner

from docs_src.commands.context import tutorial001 as mod

app = mod.app

runner = CliRunner()


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "About to execute command: create" in result.output
    assert "Creating user: Camila" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "About to execute command: delete" in result.output
    assert "Deleting user: Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
