import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.callback import tutorial004_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Manage users CLI app." in result.output
    assert "Use it with the create command." in result.output
    assert "A new user with the given NAME will be created." in result.output


def test_app():
    result = runner.invoke(app, ["create", "Camila"])
    assert result.exit_code == 0
    assert "Creating user: Camila" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
