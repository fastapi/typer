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
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.enum.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_int_enum_default(mod: ModuleType):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Access level: private (1)" in result.output


def test_int_enum(mod: ModuleType):
    result = runner.invoke(mod.app, ["--access", "open"])
    assert result.exit_code == 0
    assert "Access level: open (4)" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
