import importlib
import subprocess
import sys

import pytest
import typer
from typer import Typer
from typer.testing import CliRunner

from tests.utils import needs_py311

runner = CliRunner()


@pytest.fixture(
    name="app",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py311", marks=needs_py311),
    ],
)
def get_app(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.parameter_types.enum.{request.param}")

    app = typer.Typer()
    app.command()(mod.main)
    return app


def test_help(app: Typer):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--network" in result.output
    assert "[simple|conv|lstm]" in result.output
    assert "default: simple" in result.output


def test_main(app: Typer):
    result = runner.invoke(app, ["--network", "conv"])
    assert result.exit_code == 0
    assert "Training neural network of type: conv" in result.output


def test_main_default(app: Typer):
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Training neural network of type: simple" in result.output


def test_invalid_case(app: Typer):
    result = runner.invoke(app, ["--network", "CONV"])
    assert result.exit_code != 0
    assert "Invalid value for '--network'" in result.output
    assert "'CONV' is not one of" in result.output
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_invalid_other(app: Typer):
    result = runner.invoke(app, ["--network", "capsule"])
    assert result.exit_code != 0
    assert "Invalid value for '--network'" in result.output
    assert "'capsule' is not one of" in result.output
    assert "simple" in result.output
    assert "conv" in result.output
    assert "lstm" in result.output


def test_script(app: Typer):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
