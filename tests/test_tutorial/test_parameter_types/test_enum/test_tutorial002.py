import importlib
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from tests.utils import needs_py311

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        "tutorial002",
        "tutorial002_an",
        pytest.param("tutorial002_py311", marks=needs_py311),
    ],
)
def get_app(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.parameter_types.enum.{request.param}")
    return mod


def test_upper(mod):
    result = runner.invoke(mod.app, ["--network", "CONV"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_mix(mod):
    result = runner.invoke(mod.app, ["--network", "LsTm"])
    assert result.exit_code == 0
    assert "Training neural network of type: lstm" in result.output


def test_script(mod):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
