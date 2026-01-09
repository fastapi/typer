import importlib
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from typer.testing import CliRunner

from ....utils import needs_py310

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_py310", marks=needs_py310),
        pytest.param("tutorial003_an_py39"),
        pytest.param("tutorial003_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.version.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "Rick", "--version"])
    assert result.exit_code == 0
    assert "Awesome CLI Version: 0.1.0" in result.output


def test_2(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "rick"])
    assert result.exit_code != 0
    assert "Invalid value for '--name'" in result.output
    assert "Only Camila is allowed" in result.output


def test_3(mod: ModuleType):
    result = runner.invoke(mod.app, ["--name", "Camila"])
    assert result.exit_code == 0
    assert "Hello Camila" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout


def test_completion(mod: ModuleType):
    file_name = Path(mod.__file__).name
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            f"_{file_name.upper()}_COMPLETE": "complete_bash",
            "COMP_WORDS": f"{file_name} --name Rick --v",
            "COMP_CWORD": "3",
        },
    )
    assert "--version" in result.stdout
