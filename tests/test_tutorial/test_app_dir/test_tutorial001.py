import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from docs_src.app_dir import tutorial001_py310 as mod

runner = CliRunner()


def test_cli_config_doesnt_exist(app_dir: Path):
    result = runner.invoke(mod.app)
    assert result.exit_code == 0
    assert "Config file doesn't exist yet" in result.output


def test_cli_config_exists(app_dir: Path):
    (app_dir / "config.json").touch()
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
