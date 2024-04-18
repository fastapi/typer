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
            "tests/assets/cli/empty_script.py",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "run" not in result.stdout
