import subprocess
import sys
from unittest.mock import patch

import typer
from typer.testing import CliRunner

import docs_src.progressbar.tutorial001_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli_one_step():
    with patch("time.sleep") as sleep_mock:
        sleep_mock.side_effect = typer.Exit()  # Exit on first `time.sleep()` call
        result = runner.invoke(app)

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert result.exit_code == 0
    assert "Processing... 0%" in normalized_output


def test_cli():
    with patch("time.sleep") as mock_sleep:
        result = runner.invoke(app)

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert result.exit_code == 0
    assert mock_sleep.call_count == 100
    assert "Processing..." in normalized_output
    assert "100%" in normalized_output
    assert "Processed 100 things." in normalized_output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
