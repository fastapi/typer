import os
import subprocess
import sys

import pytest

from docs_src.commands.index import tutorial002 as sync_mod

from .for_testing import commands_index_tutorial002_async as async_mod

mod_params = ("mod", (sync_mod, async_mod))


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
            "_TYPER_COMPLETE_ARGS": f"{filename} ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create" in result.stdout
    assert "delete" in result.stdout


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
            "_TYPER_COMPLETE_ARGS": f"{filename} ",
            "_TYPER_COMPLETE_FISH_ACTION": "get-args",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create\ndelete" in result.stdout


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
            "_TYPER_COMPLETE_ARGS": f"{filename} ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create::: \ndelete::: " in result.stdout


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
            "_TYPER_COMPLETE_ARGS": f"{filename} ",
            "_TYPER_COMPLETE_TESTING": "True",
        },
    )
    assert "create::: \ndelete::: " in result.stdout
