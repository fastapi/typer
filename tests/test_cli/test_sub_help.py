import subprocess
import sys


def test_script_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/sample.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "Say bye" in result.stdout
    assert "hello" in result.stdout
    assert "Say hi" in result.stdout
