import subprocess
from pathlib import Path


def test_custom_prog_name():
    file_path = Path(__file__).parent / "assets/prog_name.py"
    result = subprocess.run(
        ["coverage", "run", str(file_path), "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage: custom-name [OPTIONS] I" in result.stdout
