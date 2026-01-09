import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

from ....utils import needs_py310

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.multiple_values.multiple_options.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code != 0
    assert "No provided users" in result.output
    assert "raw input = None" in result.output
    assert "Aborted" in result.output


def test_1_user(mod: ModuleType):
    result = runner.invoke(mod.app, ["--user", "Camila"])
    assert result.exit_code == 0
    assert "Processing user: Camila" in result.output


def test_3_user(mod: ModuleType):
    result = runner.invoke(
        mod.app, ["--user", "Camila", "--user", "Rick", "--user", "Morty"]
    )
    assert result.exit_code == 0
    assert "Processing user: Camila" in result.output
    assert "Processing user: Rick" in result.output
    assert "Processing user: Morty" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
