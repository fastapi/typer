import subprocess
import sys
from pathlib import Path


def test_set_rich_help_false_outputs_plain_text():
    file_path = Path(__file__).parent / "assets/set_rich_help.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path), "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    # assert simple help text
    assert "─" not in result.stdout


def test_set_rich_traceback_false_outputs_plain_text():
    file_path = Path(__file__).parent / "assets/set_rich_traceback.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    # assert simple help text
    assert "─" not in result.stderr
