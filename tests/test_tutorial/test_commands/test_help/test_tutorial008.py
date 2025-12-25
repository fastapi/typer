import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.help import tutorial008_py39 as mod

app = mod.app

runner = CliRunner()


def test_main_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Create a new user. ✨" in result.output
    assert "Made with ❤ in Venus" in result.output


def test_call():
    # Mainly for coverage
    result = runner.invoke(app, ["Morty"])
    assert result.exit_code == 0


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
