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
        pytest.param("tutorial005_py39"),
        pytest.param("tutorial005_an_py39"),
    ],
)
def get_mod(request: pytest.FixtureRequest) -> ModuleType:
    module_name = f"docs_src.parameter_types.file.{request.param}"
    mod = importlib.import_module(module_name)
    return mod


def test_main(tmpdir, mod: ModuleType):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma: no cover
        config_file.unlink()
        config_file.write_text("")
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    result = runner.invoke(mod.app, ["--config", f"{config_file}"])
    text = config_file.read_text()
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config line written"
    assert "This is a single line\nThis is a single line\nThis is a single line" in text


def test_script(mod: ModuleType):
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
