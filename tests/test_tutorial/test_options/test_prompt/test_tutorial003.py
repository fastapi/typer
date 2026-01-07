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
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial003_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.options.prompt.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_prompt(mod: ModuleType):
    result = runner.invoke(mod.app, input="Old Project\nOld Project\n")
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output


def test_prompt_not_equal(mod: ModuleType):
    result = runner.invoke(
        mod.app, input="Old Project\nNew Spice\nOld Project\nOld Project\n"
    )
    assert result.exit_code == 0
    assert "Error: The two entered values do not match" in result.output
    assert "Deleting project Old Project" in result.output


def test_option(mod: ModuleType):
    result = runner.invoke(mod.app, ["--project-name", "Old Project"])
    assert result.exit_code == 0
    assert "Deleting project Old Project" in result.output
    assert "Project name: " not in result.output


def test_help(mod: ModuleType):
    result = runner.invoke(mod.app, ["--help"])
    assert result.exit_code == 0
    assert "--project-name" in result.output
    assert "TEXT" in result.output
    assert "[required]" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
