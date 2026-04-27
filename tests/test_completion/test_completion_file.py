import os
import subprocess
import sys

from . import file_example as mod


def test_script() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            mod.__file__,
            "--config",
            mod.__file__,
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "def main(config: typer.FileText = typer.Option(...)):" in result.stdout


def test_completion_file_bash() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, " "],
        capture_output=True,
        encoding="utf-8",
        env={
            **os.environ,
            "_FILE_EXAMPLE.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "file_example.py --config file_ex",
            "COMP_CWORD": "2",
        },
    )
    assert result.returncode == 0
    assert "file_ex" in result.stdout
