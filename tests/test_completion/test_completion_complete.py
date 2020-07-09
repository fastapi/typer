import os
import subprocess

from docs_src.commands.help import tutorial001 as mod


def test_completion_complete_subcommand_bash():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "delete\ndelete-all" in result.stdout


def test_completion_complete_subcommand_bash_invalid():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "tutorial001.py del",
            "COMP_CWORD": "42",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create\ndelete\ndelete-all\ninit" in result.stdout


def test_completion_complete_subcommand_zsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        """_arguments '*: :(("delete":"Delete a user with USERNAME."\n"""
        """\"delete-all":"Delete ALL users in the database."))'"""
    ) in result.stdout


def test_completion_complete_subcommand_zsh_files():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py delete ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert ("_files") in result.stdout


def test_completion_complete_subcommand_fish():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete\tDelete a user with USERNAME.\ndelete-all\tDelete ALL users in the database."
        in result.stdout
    )


def test_completion_complete_subcommand_fish_should_complete():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode == 0


def test_completion_complete_subcommand_fish_should_complete_no():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py delete ",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode != 0


def test_completion_complete_subcommand_powershell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


def test_completion_complete_subcommand_pwsh():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


def test_completion_complete_subcommand_noshell():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL001.PY_COMPLETE": "complete_noshell",
            "_TYPER_COMPLETE_ARGS": "tutorial001.py del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert ("") in result.stdout
