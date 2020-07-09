import subprocess

from typer.testing import CliRunner

from docs_src.subcommands.name_help import tutorial007 as mod

runner = CliRunner()

app = mod.app


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "call-users" in result.output
    assert "Help from callback for users." in result.output


def test_command_help():
    result = runner.invoke(app, ["call-users", "--help"])
    assert result.exit_code == 0
    assert "Help from callback for users." in result.output


def test_command():
    result = runner.invoke(app, ["call-users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
