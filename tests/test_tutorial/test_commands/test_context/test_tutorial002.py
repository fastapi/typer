import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.context import tutorial002_py39 as mod

app = mod.app

runner = CliRunner()


def test_create():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Initializing database" in result.output
    assert "Creating user: Camila" in result.output


def test_delete():
    result = runner.invoke(app, ["delete", "Camila"])
    assert result.exit_code == 0
    assert "Initializing database" in result.output
    assert "Deleting user: Camila" in result.output


def test_callback():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Initializing database" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
