import os
import subprocess
import sys
from unittest import mock

import pytest
import shellingham
import typer
from typer.testing import CliRunner

from docs_src.asynchronous import tutorial001 as async_mod
from docs_src.commands.index import tutorial001 as sync_mod

runner = CliRunner()
mod_params = ("mod", (sync_mod, async_mod))


@pytest.mark.parametrize(*mod_params)
def test_completion_show_no_shell(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--show-completion"],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert "Option '--show-completion' requires an argument" in result.stderr


@pytest.mark.parametrize(*mod_params)
def test_completion_show_bash(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--show-completion",
            "bash",
        ],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "complete -o default -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_source_zsh(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--show-completion",
            "zsh",
        ],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_source_fish(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--show-completion",
            "fish",
        ],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert "complete --command tutorial001.py --no-files" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_source_powershell(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--show-completion",
            "powershell",
        ],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_source_pwsh(mod):
    app = typer.Typer()
    app.command()(mod.main)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--show-completion",
            "pwsh",
        ],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_show_invalid_shell(mod):
    app = typer.Typer()
    app.command()(mod.main)
    with mock.patch.object(
        shellingham, "detect_shell", return_value=("xshell", "/usr/bin/xshell")
    ):
        result = runner.invoke(app, ["--show-completion"])
    assert "Shell xshell not supported" in result.stdout
