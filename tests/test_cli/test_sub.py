import subprocess
import sys


def test_script_hello():
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
            "hello",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello World!" in result.stdout


def test_script_hello_name():
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
            "hello",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello Camila!" in result.stdout


def test_script_hello_name_formal():
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
            "hello",
            "--name",
            "Camila",
            "--formal",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Good morning Ms. Camila" in result.stdout


def test_script_bye():
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
            "bye",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Goodbye" in result.stdout


def test_script_bye_friend():
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
            "bye",
            "--friend",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Goodbye my friend" in result.stdout


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
