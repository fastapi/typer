import subprocess
import sys

from typer.testing import CliRunner

from docs_src.parameter_types.bytes import tutorial002 as mod

runner = CliRunner()


def test_tutorial002():
    result = runner.invoke(mod.app, ["file.txt"])
    assert result.exit_code == 0
    assert "Bytes (latin-1): b'file.txt'" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
