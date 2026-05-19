import subprocess
import sys
from unittest.mock import patch

from typer.testing import CliRunner

import docs_src.progressbar.tutorial002_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli():  # Checking only final state of spinner progress bar
    with patch("time.sleep") as mock_sleep:
        result = runner.invoke(app)

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert result.exit_code == 0
    mock_sleep.assert_called_once_with(5)
    assert "Done!" in normalized_output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
