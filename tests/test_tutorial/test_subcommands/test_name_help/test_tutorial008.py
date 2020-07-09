import subprocess

from typer.testing import CliRunner

from docs_src.subcommands.name_help import tutorial008 as mod

runner = CliRunner()

app = mod.app


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "cake-sith-users" in result.output
    assert "Unlimited powder! Eh, users." in result.output


def test_command_help():
    result = runner.invoke(app, ["cake-sith-users", "--help"])
    assert result.exit_code == 0
    assert "Unlimited powder! Eh, users." in result.output


def test_command():
    result = runner.invoke(app, ["cake-sith-users", "create", "Camila"])
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
