import subprocess
import sys

from typer.testing import CliRunner

import docs_src.printing.tutorial002_py39 as mod

app = mod.app

runner = CliRunner()


def test_cli():
    result = runner.invoke(app, color=True)
    assert result.exit_code == 0
    assert "Alert! Portal gun shooting! 💥" in result.output
    # This doesn't really test the rich formatting. Added for coverage


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
