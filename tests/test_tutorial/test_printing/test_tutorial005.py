import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial005_py310 as mod
from tests.utils import normalize_rich_output

app = mod.app

runner = CliRunner()


def test_good_true():
    result = runner.invoke(app, color=True)
    assert result.exit_code == 0

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert "everything is *good*" in normalized_output
    # We don't check exact colors here, just that text has formatting


def test_good_false():
    result = runner.invoke(app, ["--no-good"], color=True)
    assert result.exit_code == 0

    # Replace all Rich formatting with `*` characters
    normalized_output = normalize_rich_output(result.output)

    assert "everything is *bad*" in normalized_output
    # We don't check exact colors here, just that text has formatting


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
