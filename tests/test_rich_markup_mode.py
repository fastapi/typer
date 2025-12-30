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
