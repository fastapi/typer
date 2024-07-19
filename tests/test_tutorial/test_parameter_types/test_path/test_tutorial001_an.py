import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.path import tutorial001_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_no_path(tmpdir):
    Path(tmpdir) / "config.txt"
    result = runner.invoke(app)
    assert result.exit_code == 1
    assert "No config file" in result.output
    assert "Aborted" in result.output


def test_not_exists(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    if config_file.exists():  # pragma: no cover
        config_file.unlink()
    result = runner.invoke(app, ["--config", f"{config_file}"])
    assert result.exit_code == 0
    assert "The config doesn't exist" in result.output


def test_exists(tmpdir):
    config_file = Path(tmpdir) / "config.txt"
    config_file.write_text("some settings")
    result = runner.invoke(app, ["--config", f"{config_file}"])
    config_file.unlink()
    assert result.exit_code == 0
    assert "Config file contents: some settings" in result.output


def test_dir():
    result = runner.invoke(app, ["--config", "./"])
    assert result.exit_code == 0
    assert "Config is a directory, will use all its config files" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
