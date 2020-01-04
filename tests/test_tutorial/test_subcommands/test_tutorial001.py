import subprocess
import sys

from typer.testing import CliRunner

from subcommands import tutorial001
from subcommands.tutorial001 import items, users

sys.path.extend(tutorial001.__path__)  # isort:skip
from subcommands.tutorial001 import main as mod  # isort:skip


app = mod.app
runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands:" in result.output
    assert "items" in result.output
    assert "users" in result.output


def test_help_items():
    result = runner.invoke(app, ["items", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands:" in result.output
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
    assert "Commands:" in result.output
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
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_script_items():
    result = subprocess.run(
        ["coverage", "run", items.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_script_users():
    result = subprocess.run(
        ["coverage", "run", users.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
