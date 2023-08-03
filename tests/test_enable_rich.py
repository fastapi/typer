import subprocess
import sys
from pathlib import Path


def test_enable_rich_help_is_false():
    file_path = Path(__file__).parent / "assets/enable_rich.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path), "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    # assert simple help text
    assert "─" not in result.stdout


def test_enable_rich_traceback_is_false():
    file_path = Path(__file__).parent / "assets/enable_rich_traceback_false.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    # assert simple help text
    assert "─" not in result.stderr
