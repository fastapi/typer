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
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial002_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.datetime.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(mod: ModuleType):
    result = runner.invoke(mod.app, ["1969-10-29"])
    assert result.exit_code == 0
    assert "Launch will be at: 1969-10-29 00:00:00" in result.output


def test_usa_weird_date_format(mod: ModuleType):
    result = runner.invoke(mod.app, ["10/29/1969"])
    assert result.exit_code == 0
    assert "Launch will be at: 1969-10-29 00:00:00" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
