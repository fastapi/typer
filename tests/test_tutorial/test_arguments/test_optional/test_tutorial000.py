import importlib
import subprocess
import sys
from types import ModuleType

import pytest
import typer
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(
    name="mod",
    params=[
        pytest.param("tutorial000_py39"),
        pytest.param("tutorial000_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.arguments.optional.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


@pytest.fixture(name="app")
def get_app(mod: ModuleType) -> typer.Typer:
    app = typer.Typer()
    app.command()(mod.main)
    return app


def test_cli(app: typer.Typer):
    result = runner.invoke(app, ["World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output


def test_cli_missing_argument(app: typer.Typer):
    result = runner.invoke(app)
    assert result.exit_code == 2
    assert "Missing argument 'NAME'" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
