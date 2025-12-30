import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import typer
from typer.testing import CliRunner

from docs_src.launch import tutorial002_py39 as mod

runner = CliRunner()


@pytest.fixture(name="app_dir")
def app_dir():
    app_dir = Path(typer.get_app_dir("my-super-cli-app"))
    if app_dir.exists():  # pragma: no cover
        for item in app_dir.iterdir():
            if item.is_file():
                item.unlink()

    yield app_dir

    if app_dir.exists():
        for item in app_dir.iterdir():
            if item.is_file():
                item.unlink()
        app_dir.rmdir()


def test_cli(app_dir: Path):
    with patch("typer.launch") as launch_mock:
        result = runner.invoke(mod.app)

    assert result.exit_code == 0
    assert "Opening config directory" in result.output
    launch_mock.assert_called_with(str(app_dir / "config.json"), locate=True)


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
