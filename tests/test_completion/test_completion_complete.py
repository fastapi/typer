import os
import subprocess
import sys

import pytest

from docs_src.commands.help import tutorial001 as sync_mod

from .for_testing import commands_help_tutorial001_async as async_mod

mod_params = ("mod", (sync_mod, async_mod))


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_bash(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_bash",
            "COMP_WORDS": f"{filename} del",
            "COMP_CWORD": "1",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "delete\ndelete-all" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_bash_invalid(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_bash",
            "COMP_WORDS": f"{filename} del",
            "COMP_CWORD": "42",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create\ndelete\ndelete-all\ninit" in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_zsh(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        """_arguments '*: :(("delete":"Delete a user with USERNAME."\n"""
        """\"delete-all":"Delete ALL users in the database."))'"""
    ) in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_zsh_files(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": f"{filename} delete ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert ("_files") in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_fish(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete\tDelete a user with USERNAME.\ndelete-all\tDelete ALL users in the database."
        in result.stdout
    )


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_fish_should_complete(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode == 0


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_fish_should_complete_no(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": "{filename} delete ",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert result.returncode != 0


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_powershell(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_pwsh(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


@pytest.mark.parametrize(*mod_params)
def test_completion_complete_subcommand_noshell(mod):
    filename = os.path.basename(mod.__file__)
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{filename.upper()}_COMPLETE": "complete_noshell",
            "_TYPER_COMPLETE_ARGS": f"{filename} del",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "" in result.stdout
