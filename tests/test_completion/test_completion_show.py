import os
import subprocess
import sys
from unittest import mock

import shellingham
import typer
from typer.testing import CliRunner

from docs_src.commands.index import tutorial001 as mod

runner = CliRunner()
app = typer.Typer()
app.command()(mod.main)


def test_completion_show_no_shell():
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


def test_completion_show_bash():
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


def test_completion_source_zsh():
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


def test_completion_source_fish():
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


def test_completion_source_powershell():
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


def test_completion_source_pwsh():
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


def test_completion_show_invalid_shell():
    with mock.patch.object(
        shellingham, "detect_shell", return_value=("xshell", "/usr/bin/xshell")
    ):
        result = runner.invoke(app, ["--show-completion"])
    assert "Shell xshell not supported" in result.stdout
