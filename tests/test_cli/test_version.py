import subprocess
import sys


def test_script_help():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", "-m", "typer", "--version"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Typer version:" in result.stdout
