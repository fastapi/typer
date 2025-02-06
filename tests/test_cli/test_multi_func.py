import subprocess
import sys


def test_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_func.py",
            "run",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Say hi to someone, by default to the World." in result.stdout


def test_script():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello Camila" in result.stdout


def test_script_func_non_existent():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "--func",
            "non_existent",
            "tests/assets/cli/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Not a function:" in result.stderr


def test_script_func_not_function():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "--func",
            "message",
            "tests/assets/cli/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Not a function:" in result.stderr


def test_script_func():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "--func",
            "say_stuff",
            "tests/assets/cli/multi_func.py",
            "run",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello" not in result.stdout
    assert "Stuff" in result.stdout
