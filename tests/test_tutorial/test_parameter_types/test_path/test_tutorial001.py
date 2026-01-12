import importlib
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
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.path.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_no_path(tmpdir, mod: ModuleType):
    Path(tmpdir) / "config.txt"
    result = runner.invoke(mod.app)
    assert result.exit_code == 1
    assert "No config file" in result.output
    assert "Aborted" in result.output


def test_not_exists(tmpdir, mod: ModuleType):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma: no cover
        config_file.unlink()
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    assert result.exit_code == 0
    assert "The config doesn't exist" in result.output


def test_exists(tmpdir, mod: ModuleType):
    config_file = Path(tmpdir) / "config.txt"
    config_file.write_text("some settings")
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config file contents: some settings" in result.output


def test_dir(mod: ModuleType):
    result = runner.invoke(mod.app, ["--config", "./"])
    assert result.exit_code == 0
    assert "Config is a directory, will use all its config files" in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
