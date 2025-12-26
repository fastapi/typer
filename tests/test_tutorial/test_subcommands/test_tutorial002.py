import subprocess
import sys

from typer.testing import CliRunner

from docs_src.subcommands.tutorial002_py39 import main as mod

app = mod.app
runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "items" in result.output
    assert "users" in result.output


def test_help_items():
    result = runner.invoke(app, ["items", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" in result.output


def test_items_create():
    result = runner.invoke(app, ["items", "create", "Wand"])
    assert result.exit_code == 0
    assert "Creating item: Wand" in result.output


def test_items_sell():
    result = runner.invoke(app, ["items", "sell", "Vase"])
    assert result.exit_code == 0
    assert "Selling item: Vase" in result.output


def test_items_delete():
    result = runner.invoke(app, ["items", "delete", "Vase"])
    assert result.exit_code == 0
    assert "Deleting item: Vase" in result.output


def test_help_users():
    result = runner.invoke(app, ["users", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" not in result.output


def test_users_create():
    result = runner.invoke(app, ["users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_users_delete():
    result = runner.invoke(app, ["users", "delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
