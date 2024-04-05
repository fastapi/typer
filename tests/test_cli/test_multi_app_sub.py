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
            "--app",
            "sub_app",
            "tests/assets/cli/multi_app.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "hello" in result.stdout
    assert "top" not in result.stdout


def test_script():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "--app",
            "sub_app",
            "tests/assets/cli/multi_app.py",
            "run",
            "hello",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout
