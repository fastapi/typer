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
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "run" in result.stdout


def test_not_python():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/not_python.txt",
            "run",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Could not import as Python file" in result.stderr
