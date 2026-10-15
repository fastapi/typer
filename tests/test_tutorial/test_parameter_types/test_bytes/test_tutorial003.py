import subprocess
import sys

from typer.testing import CliRunner

from docs_src.parameter_types.bytes import tutorial003 as mod

runner = CliRunner()


def test_tutorial003():
    result = runner.invoke(mod.app, ["--token", "foo"])
    assert result.exit_code == 0
    assert "Token: b'foo'" in result.stdout


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
