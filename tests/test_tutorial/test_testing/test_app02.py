import subprocess

from docs_src.testing.app02 import main as mod
from docs_src.testing.app02.test_main import test_app


def test_app02():
    test_app()


def test_script():
    result = subprocess.run(
        ["coverage", "run", mod.__file__, "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
