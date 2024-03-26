import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.path import tutorial002_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_not_exists(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma: no cover
        config_file.unlink()
    result = runner.invoke(app, ["--config", f"{config_file}"])
    assert result.exit_code != 0
    assert "Invalid value for '--config': File" in result.output
    assert "does not exist" in result.output


def test_exists(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    config_file.write_text("some settings")
    result = runner.invoke(app, ["--config", f"{config_file}"])
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config file contents: some settings" in result.output


def test_dir():
    result = runner.invoke(app, ["--config", "./"])
    assert result.exit_code != 0
    assert "Invalid value for '--config': File './' is a directory." in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
