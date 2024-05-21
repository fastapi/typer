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
            "tests/assets/cli/func_other_name.py",
            "run",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Hello Camila" in result.stdout
