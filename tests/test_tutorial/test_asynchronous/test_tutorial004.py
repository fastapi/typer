import subprocess
import sys

from typer.testing import CliRunner

from docs_src.asynchronous import tutorial004 as mod

app = mod.app

runner = CliRunner()


def test_wait():
    result = runner.invoke(app, ["2"])
    assert result.exit_code == 0
    assert "Waited for 2 seconds" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
