import subprocess
import sys
import uuid

from typer.testing import CliRunner

from docs_src.parameter_types.uuid import tutorial001_py310 as mod

runner = CliRunner()
app = mod.app


def test_main():
    result = runner.invoke(app, ["d48edaa6-871a-4082-a196-4daab372d4a1"])
    assert result.exit_code == 0
    assert "User ID is d48edaa6-871a-4082-a196-4daab372d4a1" in result.output
    assert "UUID version is: 4" in result.output


def test_main_with_uuid_object():
    user_id = uuid.UUID("d48edaa6-871a-4082-a196-4daab372d4a1")
    result = runner.invoke(app, [], default_map={"user_id": user_id})
    assert result.exit_code == 0
    assert "User ID is d48edaa6-871a-4082-a196-4daab372d4a1" in result.output
    assert "UUID version is: 4" in result.output


def test_invalid_uuid():
    result = runner.invoke(app, ["7479706572-72756c6573"])
    assert result.exit_code != 0
    assert "Invalid value for 'user_id'" in result.output
    assert "should be a valid UUID" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
