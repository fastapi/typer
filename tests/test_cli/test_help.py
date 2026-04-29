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


def test_help_wrapping() -> None:
    app = typer.Typer(
        rich_markup_mode=None,
        context_settings={"max_content_width": 50},
    )

    @app.command(
        help=(
            "Wrapped paragraph has enough words to wrap in help output.\n"
            "\n"
            "\n"
            "\b\n"
            "RAW-LINE-ONE stays on one line even with many many many words.\n"
            "RAW-LINE-TWO keeps original formatting.\n"
            "\n"
            "Final paragraph wraps normally as well."
        )
    )
    def cmd() -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["cmd", "--help"], terminal_width=50)
    assert result.exit_code == 0
    assert "Wrapped paragraph has enough words to wrap" in result.output
    assert (
        "RAW-LINE-ONE stays on one line even with many many many words."
        in result.output
    )
    assert "RAW-LINE-TWO keeps original formatting." in result.output
    assert "Final paragraph wraps normally as well." in result.output


def test_help_wrapping_long_name() -> None:
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def cmd(value: str) -> None:
        pass  # pragma: no cover

    result = runner.invoke(
        app,
        ["cmd", "--help"],
        terminal_width=40,
        prog_name="very-long-program-name-that-forces-wrap",
    )
    assert result.exit_code == 0

    output_lines = result.output.splitlines()
    usage_idx = output_lines.index("Usage: very-long-program-name-that-forces-wrap ")
    args_line = output_lines[usage_idx + 1]
    assert args_line.lstrip() == "[OPTIONS] VALUE"
    assert args_line.startswith(" ")


def test_format_long_help_option() -> None:
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def cmd(
        very_long: str = typer.Option(
            ...,
            "--this-is-a-very-very-very-long-option-name",
            help="Description is rendered in the next line for long option labels.",
        ),
    ) -> None:
        pass  # pragma: no cover

    result = runner.invoke(app, ["cmd", "--help"], terminal_width=80)
    assert result.exit_code == 0

    output_lines = result.output.splitlines()
    option_idx = next(
        i
        for i, line in enumerate(output_lines)
        if "--this-is-a-very-very-very-long-option-name" in line
    )
    assert "Description is rendered" not in output_lines[option_idx]
    first_desc_line = output_lines[option_idx + 1]
    assert first_desc_line.lstrip().startswith("Description is rendered")
    continuation_block = " ".join(
        line.strip() for line in output_lines[option_idx + 1 :] if line.startswith(" ")
    )
    assert (
        "Description is rendered in the next line for long option labels."
        in continuation_block
    )
