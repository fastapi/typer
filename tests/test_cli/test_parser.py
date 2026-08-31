import subprocess
import sys

import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_double_dash() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/sample.py",
            "run",
            "hello",
            "--",
            "--name",
            "Camila",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "Got unexpected extra argument" in result.stderr
    assert "--name Camila" in result.stderr


def test_unknown_short_option() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "-m",
            "typer",
            "tests/assets/cli/sample.py",
            "run",
            "hello",
            "-x",
        ],
        capture_output=True,
        encoding="utf-8",
    )
    assert "No such option: -x" in result.stderr


def test_ignore_unknown_short_option() -> None:
    app = typer.Typer(
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True}
    )

    @app.command()
    def main(
        ctx: typer.Context, all_: bool = typer.Option(False, "--all", "-a")
    ) -> None:
        assert all_
        print(ctx.args)

    result = runner.invoke(app, ["-azq"])
    assert result.exit_code == 0
    assert "['-zq']" in result.output
