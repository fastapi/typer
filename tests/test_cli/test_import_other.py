import subprocess
import sys


def test_script():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/import_other.py",
            "run",
            "Dr. Magic",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello Dr. Magic" in result.stdout
    assert "echo: Dr. Magic" in result.stdout
