import os
import subprocess
import sys

import pytest

from docs_src.asynchronous import tutorial001 as async_mod
from docs_src.commands.index import tutorial001 as sync_mod

mod_params = ("mod", (sync_mod, async_mod))


@pytest.mark.parametrize(*mod_params)
def test_completion_show_no_shell(mod):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--show-completion"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    # TODO: when deprecating Click 7, remove second option
    assert (
        "Option '--show-completion' requires an argument" in result.stderr
        or "--show-completion option requires an argument" in result.stderr
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_show_bash(mod):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "complete -o default -F _tutorial001py_completion tutorial001.py"
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_source_zsh(mod):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert "compdef _tutorial001py_completion tutorial001.py" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_source_fish(mod):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert "complete --command tutorial001.py --no-files" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_source_powershell(mod):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_source_pwsh(mod):
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TYPER_COMPLETE_TESTING": "True",
            "_TYPER_COMPLETE_TEST_DISABLE_SHELL_DETECTION": "True",
        },
    )
    assert (
        "Register-ArgumentCompleter -Native -CommandName tutorial001.py -ScriptBlock $scriptblock"
        in result.stdout
    )
