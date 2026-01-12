from typer.testing import CliRunner

from docs_src.one_file_per_command.app_py39 import main as mod

runner = CliRunner()


def test_help():
    result = runner.invoke(mod.app, ["--help"])

    assert result.exit_code == 0

    assert "version" in result.output
    assert "users" in result.output


def test_version():
    result = runner.invoke(mod.app, ["version"])

    assert result.exit_code == 0
    assert "My CLI Version 1.0" in result.output


def test_users_help():
    result = runner.invoke(mod.app, ["users", "--help"])

    assert result.exit_code == 0

    assert "add" in result.output
    assert "delete" in result.output


def test_add_user():
    result = runner.invoke(mod.app, ["users", "add", "Camila"])

    assert result.exit_code == 0
    assert "Adding user: Camila" in result.output


def test_delete_user():
    result = runner.invoke(mod.app, ["users", "delete", "Camila"])

    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output
