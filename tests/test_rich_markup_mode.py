import os
import subprocess
import sys

import pytest
import typer
import typer.completion
from typer.testing import CliRunner

runner = CliRunner()
rounded = ["╭", "─", "┬", "╮", "│", "├", "┼", "┤", "╰", "┴", "╯"]


def test_rich_markup_mode_none():
    app = typer.Typer(rich_markup_mode=None)

    @app.command()
    def main(arg: str):
        """Main function"""
        print(f"Hello {arg}")

    assert app.rich_markup_mode is None

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    assert "arg  [required]" in result.stdout
    assert all(c not in result.stdout for c in rounded)


def test_rich_markup_mode_rich():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(arg: str):
        """Main function"""
        print(f"Hello {arg}")

    assert app.rich_markup_mode == "rich"

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    assert any(c in result.stdout for c in rounded)


@pytest.mark.parametrize(
    "env_var_value, expected_result",
    [
        ("1", True),
        ("True", True),
        ("TRUE", True),
        ("true", True),
        ("0", False),
        ("False", False),
        ("FALSE", False),
        ("false", False),
        ("somerandomvalue", True),
    ],
)
def test_rich_markup_mode_envvar(env_var_value: str, expected_result: bool):
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
        env={
            **os.environ,
            "TYPER_USE_RICH": env_var_value,
            "PYTHONIOENCODING": "utf-8",
        },
        encoding="utf-8",
    )
    assert any(c in result.stdout for c in rounded) == expected_result


@pytest.mark.parametrize(
    "mode,lines",
    [
        pytest.param(
            "markdown",
            ["First line", "", "Line 1", "", "Line 2", "", "Line 3", ""],
        ),
        pytest.param(
            "rich", ["First line", "", "Line 1", "", "Line 2", "", "Line 3", ""]
        ),
        pytest.param(
            None, ["First line", "", "Line 1", "", "Line 2", "", "Line 3", ""]
        ),
    ],
)
def test_markup_mode_newline_pr815(mode: str, lines: list[str]):
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def main(arg: str):
        """First line

        Line 1

        Line 2

        Line 3
        """
        print(f"Hello {arg}")

    assert app.rich_markup_mode == mode

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    result_lines = [line.strip() for line in result.stdout.split("\n")]
    if mode:
        assert any(c in result.stdout for c in rounded)
    help_start = result_lines.index("First line")
    arg_start = [i for i, row in enumerate(result_lines) if "Arguments" in row][0]
    assert help_start != -1
    assert result_lines[help_start:arg_start] == lines


@pytest.mark.parametrize(
    "mode,lines",
    [
        pytest.param("markdown", ["First line", "", "Line 1 Line 2 Line 3", ""]),
        pytest.param("rich", ["First line", "", "Line 1", "Line 2", "Line 3", ""]),
        pytest.param(None, ["First line", "", "Line 1 Line 2 Line 3", ""]),
    ],
)
def test_markup_mode_newline_issue447(mode: str, lines: list[str]):
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def main(arg: str):
        """First line

        Line 1
        Line 2
        Line 3
        """
        print(f"Hello {arg}")

    assert app.rich_markup_mode == mode

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    result_lines = [line.strip() for line in result.stdout.split("\n")]
    if mode:
        assert any(c in result.stdout for c in rounded)
    help_start = result_lines.index("First line")
    arg_start = [i for i, row in enumerate(result_lines) if "Arguments" in row][0]
    assert help_start != -1
    assert result_lines[help_start:arg_start] == lines


@pytest.mark.parametrize(
    "mode,lines",
    [
        pytest.param(
            "markdown",
            [
                "This header is long",
                "",
                "Line 1",
                "",
                "Line 2 continues here",
                "",
                "Line 3",
                "",
            ],
        ),
        pytest.param(
            "rich",
            [
                "This header is long",
                "",
                "Line 1",
                "",
                "Line 2",
                "continues here",
                "",
                "Line 3",
                "",
            ],
        ),
        pytest.param(
            None,
            [
                "This header is long",
                "",
                "Line 1",
                "",
                "Line 2 continues here",
                "",
                "Line 3",
                "",
            ],
        ),
    ],
)
def test_markup_mode_newline_mixed(mode: str, lines: list[str]):
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def main(arg: str):
        """This header
        is long

        Line 1

        Line 2
        continues here

        Line 3
        """
        print(f"Hello {arg}")

    assert app.rich_markup_mode == mode

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    result_lines = [line.strip() for line in result.stdout.split("\n")]
    if mode:
        assert any(c in result.stdout for c in rounded)
    help_start = [i for i, row in enumerate(result_lines) if "This header" in row][0]
    arg_start = [i for i, row in enumerate(result_lines) if "Arguments" in row][0]
    assert help_start != -1
    assert result_lines[help_start:arg_start] == lines


@pytest.mark.parametrize(
    "mode,lines",
    [
        pytest.param(
            "markdown",
            ["First line", "", "• 1", "• 2", "• 3", ""],
            marks=pytest.mark.xfail,
        ),
        pytest.param("rich", ["First line", "", "- 1", "- 2", "- 3", ""]),
        pytest.param(None, ["First line", "", "- 1 - 2 - 3", ""]),
    ],
)
def test_markup_mode_bullets_single_newline(mode: str, lines: list[str]):
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def main(arg: str):
        """First line

        - 1
        - 2
        - 3
        """
        print(f"Hello {arg}")

    assert app.rich_markup_mode == mode

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    result_lines = [line.strip() for line in result.stdout.split("\n")]
    if mode:
        assert any(c in result.stdout for c in rounded)
    help_start = result_lines.index("First line")
    arg_start = [i for i, row in enumerate(result_lines) if "Arguments" in row][0]
    assert help_start != -1
    assert result_lines[help_start:arg_start] == lines


@pytest.mark.parametrize(
    "mode,lines",
    [
        pytest.param(
            "markdown",
            ["First line", "", "• 1", "• 2", "• 3", ""],
            marks=pytest.mark.xfail,
        ),
        (
            "rich",
            ["First line", "", "- 1", "", "- 2", "", "- 3", ""],
        ),
        (None, ["First line", "", "- 1", "", "- 2", "", "- 3", ""]),
    ],
)
def test_markup_mode_bullets_double_newline(mode: str, lines: list[str]):
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def main(arg: str):
        """First line

        - 1

        - 2

        - 3
        """
        print(f"Hello {arg}")

    assert app.rich_markup_mode == mode

    result = runner.invoke(app, ["World"])
    assert "Hello World" in result.stdout

    result = runner.invoke(app, ["--help"])
    result_lines = [line.strip() for line in result.stdout.split("\n")]
    if mode:
        assert any(c in result.stdout for c in rounded)
    help_start = result_lines.index("First line")
    arg_start = [i for i, row in enumerate(result_lines) if "Arguments" in row][0]
    assert help_start != -1
    assert result_lines[help_start:arg_start] == lines


def test_markup_mode_default():
    # We're assuming the test suite is run with rich installed
    app = typer.Typer()
    assert app.rich_markup_mode == "rich"


@pytest.mark.parametrize(
    "mode,expected_collapsed",
    [
        pytest.param("rich", True),
        pytest.param("markdown", True),
    ],
)
def test_commands_panel_single_newline_collapsed(mode: str, expected_collapsed: bool):
    """Single newlines in a subcommand's help should be collapsed to spaces in the
    commands panel (the summary line shown next to each command name in a group's
    --help output), regardless of markup_mode.

    In rich mode, _make_command_help previously used ``markup_mode != MARKUP_MODE_RICH``
    (inverted) so single newlines were *not* collapsed, causing multi-line rows in the
    commands table.  The fix aligns the condition with _get_help_text and
    _get_parameter_help, which both use ``markup_mode != MARKUP_MODE_MARKDOWN``.
    """
    app = typer.Typer(rich_markup_mode=mode)

    @app.command()
    def cmd1():
        """First line
        second line"""
        pass  # pragma: no cover

    @app.command()
    def cmd2():
        """Normal help"""
        pass  # pragma: no cover

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0

    # The commands panel must show "First line second line" on a single row.
    # If the bug is present, "second line" appears on a separate row without a
    # command name, i.e. the stripped line "second line" exists in the output.
    stripped_lines = [line.strip() for line in result.stdout.split("\n")]
    # "second line" must appear as part of the same row as "cmd1", not standalone.
    assert "second line" not in stripped_lines, (
        f"In {mode!r} mode, 'second line' appeared as a standalone stripped line, "
        "meaning single newlines were not collapsed in the commands panel."
    )
    # The collapsed text should appear somewhere in the output.
    assert "First line second line" in result.stdout, (
        f"In {mode!r} mode, the collapsed text 'First line second line' was not found "
        "in the commands panel output."
    )
