import importlib
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial007_py39"),
        pytest.param("tutorial007_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options_autocompletion.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_completion(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": f"{file_name} --name Sebastian --name ",
        },
    )
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout
    assert '"Sebastian":"The type hints guy."' not in result.stdout


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "Camila", "--name", "Sebastian"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "Hello Sebastian" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
