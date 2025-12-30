import subprocess
import sys

from typer.testing import CliRunner

from docs_src.prompt import tutorial003_py39 as mod

runner = CliRunner()
app = mod.app


def test_cli():
    result = runner.invoke(app, input="y\n")
    assert result.exit_code == 0
    assert "Are you sure you want to delete it? [y/N]:" in result.output
    assert "Deleting it!" in result.output


def test_no_confirm():
    result = runner.invoke(app, input="n\n")
    assert result.exit_code == 1
    assert "Are you sure you want to delete it? [y/N]:" in result.output
    assert "Aborted" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
