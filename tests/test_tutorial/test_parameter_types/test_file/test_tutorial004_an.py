import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.file import tutorial004_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main(tmpdir):
    binary_file = Path(tmpdir) / "config.txt"
    if binary_file.exists():  # pragma: no cover
        binary_file.unlink()
    result = runner.invoke(app, ["--file", f"{binary_file}"])
    text = binary_file.read_text()
    binary_file.unlink()
    assert result.exit_code == 0
    assert "Binary file written" in result.output
    assert "some settings" in text
    assert "la cigüeña trae al niño" in text


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
