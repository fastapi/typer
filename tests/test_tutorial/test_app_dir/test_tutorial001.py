import subprocess
import sys
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

from docs_src.app_dir import tutorial001_py39 as mod

runner = CliRunner()


@pytest.fixture(name="config_file")
def create_config_file():
    app_dir = Path(typer.get_app_dir("my-super-cli-app"))
    app_dir.mkdir(parents=True, exist_ok=True)
    config_path = app_dir / "config.json"
    config_path.touch(exist_ok=True)

    yield config_path

    config_path.unlink()
    app_dir.rmdir()


def test_cli_config_doesnt_exist():
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Config file doesn't exist yet" in result.output


def test_cli_config_exists(config_file: Path):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Config file doesn't exist yet" not in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
