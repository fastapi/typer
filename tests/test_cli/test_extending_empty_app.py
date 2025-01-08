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
            "tests/assets/cli/extended_empty_app_cli.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "hello" in result.stdout


def test_script_hello():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/extended_empty_app_cli.py",
            "run",
            "hello",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "hello there" in result.stdout


def test_script_bye():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/extended_empty_app_cli.py",
            "run",
            "bye",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
