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
    assert "Arguments:" in result.stdout  # as opposed to 'Arguments' without ':'
    # like in the Rich Panels
