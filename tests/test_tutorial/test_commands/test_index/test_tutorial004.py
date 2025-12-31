import subprocess
import sys

from typer.testing import CliRunner

from docs_src.commands.index import tutorial004_py39 as mod

app = mod.app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[OPTIONS] COMMAND [ARGS]..." in result.output
    print(result.output)
    assert "Commands" in result.output
    assert "create" in result.output
    assert "delete" in result.output
    # Test that the 'delete' command precedes the 'create' command in the help output
    create_char = result.output.index("create")
    delete_char = result.output.index("delete")
    assert delete_char < create_char


def test_create():
    result = runner.invoke(app, ["create"])
    assert result.exit_code == 0
    assert "Creating user: Hiro Hamada" in result.output


def test_delete():
    result = runner.invoke(app, ["delete"])
    assert result.exit_code == 0
    assert "Deleting user: Hiro Hamada" in result.output


def test_script():
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", mod.__file__, "--help"],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Usage" in result.stdout
