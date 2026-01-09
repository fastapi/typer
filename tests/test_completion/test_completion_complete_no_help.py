import os
import subprocess
import sys

from docs_src.commands.index import tutorial002_py39 as mod


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002_PY39.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial002_py39.py ",
        },
    )
    assert "create" in result.stdout
    assert "delete" in result.stdout


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002_PY39.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial002_py39.py ",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
        },
    )
    assert "create\ndelete" in result.stdout


def test_completion_complete_subcommand_powershell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002_PY39.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "tutorial002_py39.py ",
        },
    )
    assert ("create::: \ndelete::: ") in result.stdout


def test_completion_complete_subcommand_pwsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002_PY39.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "tutorial002_py39.py ",
        },
    )
    assert ("create::: \ndelete::: ") in result.stdout
