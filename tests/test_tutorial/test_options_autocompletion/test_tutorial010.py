import importlib
import os
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial010_py39"),
        pytest.param("tutorial010_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options_autocompletion.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_completion(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL010.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial010.py --user Sebastian --user ",
        },
    )
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout
    assert '"Sebastian":"The type hints guy."' not in result.stdout


def test_completion_greeter1(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL010.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial010.py --user Sebastian --greeter Ca",
        },
    )
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' in result.stdout
    assert '"Sebastian":"The type hints guy."' not in result.stdout


def test_completion_greeter2(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_TUTORIAL010.PY_COMPLETE": "complete_zsh",
            "_TYPER_COMPLETE_ARGS": "tutorial010.py --user Sebastian --greeter Carlos --greeter ",
        },
    )
    assert '"Camila":"The reader of books."' in result.stdout
    assert '"Carlos":"The writer of scripts."' not in result.stdout
    assert '"Sebastian":"The type hints guy."' in result.stdout


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--user", "Camila", "--user", "Sebastian"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output
    assert "Hello Sebastian" in result.output


def test_2(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--user", "Camila", "--user", "Sebastian", "--greeter", "Carlos"]
    )
    assert result.exit_code == 0
    assert "Hello Camila, from Carlos" in result.output
    assert "Hello Sebastian, from Carlos" in result.output


def test_3(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--user", "Camila", "--greeter", "Carlos", "--greeter", "Sebastian"]
    )
    assert result.exit_code == 0
    assert "Hello Camila, from Carlos and Sebastian" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
