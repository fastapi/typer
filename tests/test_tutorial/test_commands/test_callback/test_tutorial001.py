import subprocess

from typer.testing import CliRunner

from docs_src.commands.callback import tutorial001 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Manage users in the awesome CLI app." in result.output
    assert "--verbose / --no-verbose" in result.output


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_create_verbose():
    result = runner.invoke(app, ["--verbose", "create", "Camila"])
    assert result.exit_code == 0
    assert "Will write verbose output" in result.output
    assert "About to create a user" in result.output
    assert "Creating user: Camila" in result.output
    assert "Just created a user" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_delete_verbose():
    result = runner.invoke(app, ["--verbose", "delete", "Camila"])
    assert result.exit_code == 0
    assert "Will write verbose output" in result.output
    assert "About to delete a user" in result.output
    assert "Deleting user: Camila" in result.output
    assert "Just deleted a user" in result.output


def test_wrong_verbose():
    result = runner.invoke(app, ["delete", "--verbose", "Camila"])
    assert result.exit_code != 0
    # TODO: when deprecating Click 7, remove second option
    assert (
        "Error: No such option: --verbose" in result.output
        or "Error: no such option: --verbose" in result.output
    )


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
