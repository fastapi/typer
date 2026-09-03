import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from docs_src.launch import tutorial002_py310 as mod

runner = CliRunner()


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
