import subprocess
import sys
from pathlib import Path

import typer
from typer.testing import CliRunner

from docs_src.parameter_types.file import tutorial003_an as mod

runner = CliRunner()

app = typer.Typer()
app.command()(mod.main)


def test_main(tmpdir):
    binary_file = Path(tmpdir) / "config.txt"
    binary_file.write_bytes(b"la cig\xc3\xbce\xc3\xb1a trae al ni\xc3\xb1o")
    result = runner.invoke(app, ["--file", f"{binary_file}"])
    binary_file.unlink()
    assert result.exit_code == 0
    assert "Processed bytes total:" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
