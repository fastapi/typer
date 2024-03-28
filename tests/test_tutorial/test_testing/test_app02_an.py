import subprocess
import sys

from docs_src.testing.app02_an import main as mod
from docs_src.testing.app02_an.test_main import test_app


def test_app02_an():
    test_app()


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
