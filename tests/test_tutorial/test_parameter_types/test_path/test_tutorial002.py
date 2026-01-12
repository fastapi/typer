import importlib
import subprocess
import sys
from pathlib import Path
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
    module_name = f"docs_src.parameter_types.path.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_not_exists(tmpdir, mod: ModuleType):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma: no cover
        config_file.unlink()
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    assert result.exit_code != 0
    assert "Invalid value for '--config'" in result.output
    assert "File" in result.output
    assert "does not exist" in result.output


def test_exists(tmpdir, mod: ModuleType):
    config_file = Path(tmpdir) / "config.txt"
    config_file.write_text("some settings")
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config file contents: some settings" in result.output


def test_dir(mod: ModuleType):
    result = runner.invoke(mod.app, ["--config", "./"])
    assert result.exit_code != 0
    assert "Invalid value for '--config'" in result.output
    assert "File './' is a directory." in result.output


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
