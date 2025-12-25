import subprocess
import sys
from unittest.mock import patch

from typer.testing import CliRunner

from docs_src.launch import tutorial001_py39 as mod

runner = CliRunner()


def test_cli():
    with patch("typer.launch") as launch_mock:
        result = runner.invoke(mod.app)

    assert result.exit_code == 0
    assert result.output.strip() == "Opening Typer's docs"
    launch_mock.assert_called_once_with("https://typer.tiangolo.com")


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
