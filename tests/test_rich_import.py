import subprocess
import sys
from pathlib import Path

ACCEPTED_MODULES = {"rich._extension", "rich"}


def test_rich_not_imported_unnecessary():
    file_path = Path(__file__).parent / "assets/print_modules.py"
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", str(file_path)],
        capture_output=True,
        encoding="utf-8",
    )
    modules = result.stdout.splitlines()
    modules = [
        module
        for module in modules
        if module not in ACCEPTED_MODULES and module.startswith("rich")
    ]
    assert not modules
