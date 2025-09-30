import subprocess

import pytest
from typer.testing import CliRunner

from docs_src.subcommands import tutorial004

runner = CliRunner()


@pytest.fixture()
def mod(monkeypatch):
    with monkeypatch.context() as m:
        monkeypatch.syspath_prepend(list(tutorial004.__path__)[0])
        from docs_src.subcommands.tutorial004 import main

        return main


@pytest.fixture()
def app(mod):
    return mod.app


def test_help(app):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "remote" in result.output


def test_help_remote(app):
    result = runner.invoke(app, ["remote", "--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    assert "Commands" in result.output
    assert "add" in result.output


def test_help_remote_add(app):
    result = runner.invoke(app, ["remote", "add", "--help"])
    assert result.exit_code == 0
    assert "BRANCH" in result.output
    assert "URL" in result.output


def test_remote_call(app):
    result = runner.invoke(app, ["remote"])
    assert result.exit_code == 0
    assert "This is the remote main command" in result.output


def test_remote_add_call(app):
    result = runner.invoke(app, ["remote", "add", "branch", "url"])
    assert result.exit_code == 0
    assert "Adding remote branch with url url" in result.output


def test_scripts(mod):
    from docs_src.subcommands.tutorial004 import main

    for module in [mod, main]:
        result = subprocess.run(
            ["coverage", "run", module.__file__, "--help"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )
        assert "Usage" in result.stdout
