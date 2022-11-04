import subprocess

from typer.testing import CliRunner

from docs_src.commands.help import tutorial003 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create" in result.output
    assert "Create a user." in result.output
    assert "delete" in result.output
    assert "(deprecated)" in result.output
    assert "Delete a user." in result.output


def test_help_delete():
    result = runner.invoke(app, ["delete", "--help"])
    assert result.exit_code == 0
    assert "(deprecated)" in result.output
    assert "Delete a user." in result.output


def test_call():
    # Mainly for coverage
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
