import subprocess
import sys

from typer.testing import CliRunner

from docs_src.parameter_types.uuid import tutorial001_py39 as mod

runner = CliRunner()
app = mod.app


def test_main():
    result = runner.invoke(app, ["d48edaa6-871a-4082-a196-4daab372d4a1"])
    assert result.exit_code == 0
    assert "USER_ID is d48edaa6-871a-4082-a196-4daab372d4a1" in result.output
    assert "UUID version is: 4" in result.output


def test_invalid_uuid():
    result = runner.invoke(app, ["7479706572-72756c6573"])
    assert result.exit_code != 0
    assert (
        "Invalid value for 'USER_ID': '7479706572-72756c6573' is not a valid UUID"
        in result.output
    )


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
