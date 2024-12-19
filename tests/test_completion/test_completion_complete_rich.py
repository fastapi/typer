import os
import subprocess
import sys

from . import tutorial001_with_rich_tags as mod


def test_completion_complete_subcommand_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_WITH_RICH_TAGS.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial001_with_rich_tags.py del",
            "COMP_CWORD": "1",
        },
    )
    assert "delete\ndelete-all" in result.stdout


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_WITH_RICH_TAGS.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial001_with_rich_tags.py del",
        },
    )
    assert (
        """_arguments '*: :(("delete":"Delete a user with USERNAME."\n"""
        """\"delete-all":"Delete ALL users in the database."))'"""
    ) in result.stdout


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_WITH_RICH_TAGS.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial001_with_rich_tags.py del",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
        },
    )
    assert (
        "delete\tDelete a user with USERNAME.\ndelete-all\tDelete ALL users in the database."
        in result.stdout
    )


def test_completion_complete_subcommand_powershell():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_WITH_RICH_TAGS.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "tutorial001_with_rich_tags.py del",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


def test_completion_complete_subcommand_pwsh():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001_WITH_RICH_TAGS.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "tutorial001_with_rich_tags.py del",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout
