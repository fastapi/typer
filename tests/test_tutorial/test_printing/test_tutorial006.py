import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial006_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_cli():
    result = runner.invoke(app, ["everyone"], color=True)
    assert result.exit_code == 0

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert "*Welcome here everyone*" in normalized_output
    # We don't check exact colors here, just that text has formatting


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
