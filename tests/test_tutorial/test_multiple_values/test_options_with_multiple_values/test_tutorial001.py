import importlib
import subprocess
import sys
from types import ModuleType

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = (
        f"docs_src.multiple_values.options_with_multiple_values.{request.param}"
    )
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code != 0
    assert "No user provided" in result.output
    assert "Aborted" in result.output


def test_user_1(mod: ModuleType):
    result = runner.invoke(mod.app, ["--user", "Camila", "50", "yes"])
    assert result.exit_code == 0
    assert "The username Camila has 50 coins" in result.output
    assert "And this user is a wizard!" in result.output


def test_user_2(mod: ModuleType):
    result = runner.invoke(mod.app, ["--user", "Morty", "3", "no"])
    assert result.exit_code == 0
    assert "The username Morty has 3 coins" in result.output
    assert "And this user is a wizard!" not in result.output


def test_invalid_user(mod: ModuleType):
    result = runner.invoke(mod.app, ["--user", "Camila", "50"])
    assert result.exit_code != 0
    assert "Option '--user' requires 3 arguments" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
