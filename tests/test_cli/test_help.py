import subprocess
import sys

import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_script_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/sample.py",
            "--help",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "run" in result.stdout


def test_not_python():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/not_python.txt",
            "run",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Could not import as Python file" in result.stderr


def test_short_help() -> None:
    app = typer.Typer(
        rich_markup_mode=None,
        context_settings={"max_content_width": 50},
    )

    @app.command(help=" \n\t ")
    def empty() -> None:
        pass  # pragma: no cover

    @app.command(help="\b first sentence.")
    def marker() -> None:
        pass  # pragma: no cover

    # Forcing truncation
    @app.command(help=f"{'x' * 30} {'y' * 5} z trailing")
    def long() -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"], terminal_width=50)
    assert result.exit_code == 0
    assert "empty" in result.output
    assert "marker" in result.output
    assert "long" in result.output
    assert "first sentence." in result.output
    assert f"{'x' * 30}..." in result.output
