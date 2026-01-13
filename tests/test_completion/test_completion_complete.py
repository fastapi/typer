import importlib
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.commands.help.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_completion_complete_subcommand_bash(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_bash",
            "COMP_WORDS": f"{file_name} del",
            "COMP_CWORD": "1",
        },
    )
    print(result)
    assert "delete\ndelete-all" in result.stdout


def test_completion_complete_subcommand_bash_invalid(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_bash",
            "COMP_WORDS": f"{file_name} del",
            "COMP_CWORD": "42",
        },
    )
    assert "create\ndelete\ndelete-all\ninit" in result.stdout


def test_completion_complete_subcommand_zsh(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
        },
    )
    assert (
        """_arguments '*: :(("delete":"Delete a user with USERNAME."\n"""
        """\"delete-all":"Delete ALL users in the database."))'"""
    ) in result.stdout


def test_completion_complete_subcommand_zsh_files(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": f"{file_name} delete ",
        },
    )
    assert ("_files") in result.stdout


def test_completion_complete_subcommand_fish(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
        },
    )
    assert (
        "delete\tDelete a user with USERNAME.\ndelete-all\tDelete ALL users in the database."
        in result.stdout
    )


def test_completion_complete_subcommand_fish_should_complete(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
        },
    )
    assert result.returncode == 0


def test_completion_complete_subcommand_fish_should_complete_no(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_fish",
            "_TYPER_COMPLETE_ARGS": f"{file_name} delete ",
            "_TYPER_COMPLETE_FISH_ACTION": "is-args",
        },
    )
    assert result.returncode != 0


def test_completion_complete_subcommand_powershell(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_powershell",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


def test_completion_complete_subcommand_pwsh(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_pwsh",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
        },
    )
    assert (
        "delete:::Delete a user with USERNAME.\ndelete-all:::Delete ALL users in the database."
    ) in result.stdout


def test_completion_complete_subcommand_noshell(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_noshell",
            "_TYPER_COMPLETE_ARGS": f"{file_name} del",
        },
    )
    assert ("") in result.stdout
