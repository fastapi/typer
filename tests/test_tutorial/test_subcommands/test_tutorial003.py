import os
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from docs_src.subcommands import tutorial003_py39
from docs_src.subcommands.tutorial003_py39 import items, users

runner = CliRunner()


@pytest.fixture()
def mod(monkeypatch):
    with monkeypatch.context() as m:
        m.syspath_prepend(list(tutorial003_py39.__path__)[0])
        from docs_src.subcommands.tutorial003_py39 import main

        return main


@pytest.fixture()
def app(mod):
    return mod.app


def test_help(app):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "items" in result.output
    assert "users" in result.output
    assert "lands" in result.output


def test_help_items(app):
    result = runner.invoke(app, ["items", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" in result.output


def test_items_create(app):
    result = runner.invoke(app, ["items", "create", "Wand"])
    assert result.exit_code == 0
    assert "Creating item: Wand" in result.output
    # For coverage, because the monkeypatch above sometimes confuses coverage
    result = runner.invoke(items.app, ["create", "Wand"])
    assert result.exit_code == 0
    assert "Creating item: Wand" in result.output


def test_items_sell(app):
    result = runner.invoke(app, ["items", "sell", "Vase"])
    assert result.exit_code == 0
    assert "Selling item: Vase" in result.output
    # For coverage, because the monkeypatch above sometimes confuses coverage
    result = runner.invoke(items.app, ["sell", "Vase"])
    assert result.exit_code == 0
    assert "Selling item: Vase" in result.output


def test_items_delete(app):
    result = runner.invoke(app, ["items", "delete", "Vase"])
    assert result.exit_code == 0
    assert "Deleting item: Vase" in result.output
    # For coverage, because the monkeypatch above sometimes confuses coverage
    result = runner.invoke(items.app, ["delete", "Vase"])
    assert result.exit_code == 0
    assert "Deleting item: Vase" in result.output


def test_help_users(app):
    result = runner.invoke(app, ["users", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    assert "sell" not in result.output


def test_users_create(app):
    result = runner.invoke(app, ["users", "create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output
    # For coverage, because the monkeypatch above sometimes confuses coverage
    result = runner.invoke(users.app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_users_delete(app):
    result = runner.invoke(app, ["users", "delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output
    # For coverage, because the monkeypatch above sometimes confuses coverage
    result = runner.invoke(users.app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Deleting user: Camila" in result.output


def test_help_lands(app):
    result = runner.invoke(app, ["lands", "--help"])
    assert result.exit_code == 0
    assert "lands [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "reigns" in result.output
    assert "towns" in result.output


def test_help_lands_reigns(app):
    result = runner.invoke(app, ["lands", "reigns", "--help"])
    assert result.exit_code == 0
    assert "lands reigns [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "conquer" in result.output
    assert "destroy" in result.output


def test_lands_reigns_conquer(app):
    result = runner.invoke(app, ["lands", "reigns", "conquer", "Gondor"])
    assert result.exit_code == 0
    assert "Conquering reign: Gondor" in result.output


def test_lands_reigns_destroy(app):
    result = runner.invoke(app, ["lands", "reigns", "destroy", "Mordor"])
    assert result.exit_code == 0
    assert "Destroying reign: Mordor" in result.output


def test_help_lands_towns(app):
    result = runner.invoke(app, ["lands", "towns", "--help"])
    assert result.exit_code == 0
    assert "lands towns [OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "burn" in result.output
    assert "found" in result.output


def test_lands_towns_found(app):
    result = runner.invoke(app, ["lands", "towns", "found", "Cartagena"])
    assert result.exit_code == 0
    assert "Founding town: Cartagena" in result.output


def test_lands_towns_burn(app):
    result = runner.invoke(app, ["lands", "towns", "burn", "New Asgard"])
    assert result.exit_code == 0
    assert "Burning town: New Asgard" in result.output


def test_scripts(mod):
    from docs_src.subcommands.tutorial003_py39 import items, lands, reigns, towns, users

    env = os.environ.copy()
    env["PYTHONPATH"] = ":".join(list(tutorial003_py39.__path__))

    for module in [mod, items, lands, reigns, towns, users]:
        result = subprocess.run(
            [sys.executable, "-m", "coverage", "run", module.__file__, "--help"],
            capture_output=True,
            encoding="utf-8",
            env=env,
        )
        assert "Usage" in result.stdout
