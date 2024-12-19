import os
import subprocess
import sys

from . import example_rich_tags as mod


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "create", "DeadPool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "Creating user: DeadPool" in result.stdout

    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "delete", "DeadPool"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "Deleting user: DeadPool" in result.stdout

    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "delete-all"],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "Deleting all users" in result.stdout


def test_completion_complete_subcommand_bash():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_EXAMPLE_RICH_TAGS.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "example_rich_tags.py del",
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
            "_EXAMPLE_RICH_TAGS.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "example_rich_tags.py del",
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
            "_EXAMPLE_RICH_TAGS.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "example_rich_tags.py del",
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
            "_EXAMPLE_RICH_TAGS.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "example_rich_tags.py del",
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
            "_EXAMPLE_RICH_TAGS.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "example_rich_tags.py del",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout
