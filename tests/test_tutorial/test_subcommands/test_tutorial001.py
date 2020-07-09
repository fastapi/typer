import subprocess

import pytest
from typer.testing import CliRunner

from docs_src.subcommands import tutorial001

runner = CliRunner()


@pytest.fixture()
def mod(monkeypatch):
    with monkeypatch.context() as m:
        monkeypatch.syspath_prepend(list(tutorial001.__path__)[0])
        from docs_src.subcommands.tutorial001 import main

        return main


@pytest.fixture()
def app(mod):
    return mod.app


def test_help(app):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands:" in result.output
    assert "items" in result.output
    assert "users" in result.output


def test_help_items(app):
    result = runner.invoke(app, ["items", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands:" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" in result.output


def test_items_create(app):
    result = runner.invoke(app, ["items", "create", "Wand"])
    assert result.exit_code == 0
    assert "Creating item: Wand" in result.output


def test_items_sell(app):
    result = runner.invoke(app, ["items", "sell", "Vase"])
    assert result.exit_code == 0
    assert "Selling item: Vase" in result.output


def test_items_delete(app):
    result = runner.invoke(app, ["items", "delete", "Vase"])
    assert result.exit_code == 0
    assert "Deleting item: Vase" in result.output


def test_help_users(app):
    result = runner.invoke(app, ["users", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands:" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" not in result.output


def test_users_create(app):
    result = runner.invoke(app, ["users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_users_delete(app):
    result = runner.invoke(app, ["users", "delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_scripts(mod):
    from docs_src.subcommands.tutorial001 import items, users

    for module in [mod, items, users]:
        result = subprocess.run(
            ["coverage", "run", module.__file__, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        assert "Usage" in result.stdout
