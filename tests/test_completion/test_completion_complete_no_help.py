import os
import subprocess

from docs_src.commands.index import tutorial002 as mod


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial002.py ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create" in result.stdout
    assert "delete" in result.stdout


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial002.py ",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create\ndelete" in result.stdout


def test_completion_complete_subcommand_powershell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "tutorial002.py ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert ("create::: \ndelete::: ") in result.stdout


def test_completion_complete_subcommand_pwsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL002.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "tutorial002.py ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert ("create::: \ndelete::: ") in result.stdout
