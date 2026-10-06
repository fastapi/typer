import re
from typing import Annotated

import pytest
import typer
from typer._click.exceptions import NoSuchOption
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(params=["rich", None], ids=["rich", "plain"])
def app(request: pytest.FixtureRequest) -> typer.Typer:
    app = typer.Typer(add_completion=False, rich_markup_mode=request.param)

    @app.command()
    def no_args() -> None:
        pass  # pragma: no cover

    @app.command()
    def read_file(value: typer.FileText) -> None:
        pass  # pragma: no cover

    @app.command()
    def parse(
        value: Annotated[int, typer.Argument(parser=lambda x: int(x, 0))],
    ) -> None:
        pass  # pragma: no cover

    return app


@pytest.mark.parametrize("color", [False, True])
@pytest.mark.parametrize(
    ("command", "prefix", "message"),
    [
        ("no-args", "", "Got unexpected extra argument(s)"),
        ("no-args", "--", "No such option"),
        ("read-file", "", "Invalid value"),
        ("parse", "", "Invalid value"),
    ],
    ids=["extra-argument", "unknown-option", "file-open", "custom-parser"],
)
@pytest.mark.parametrize(
    ("value", "escaped"),
    [
        ("\x1b[2J\x1b[H", r"\x1b[2J\x1b[H"),
        ("\x1b]52;c;YWJj\x07", r"\x1b]52;c;YWJj\x07"),
        ("\x1b]52;c;YWJj\x1b\\", "\\x1b]52;c;YWJj\\x1b\\"),
        ("\x9b2J\x9d52;c;YWJj\x9c", r"\x9b2J\x9d52;c;YWJj\x9c"),
        ("\r\n\t\b\x7f", r"\x0d\x0a\x09\x08\x7f"),
        (
            "text-\u00e9-\u65e5\u672c-\U0001f469\u200d\U0001f4bb-'quoted'-\\text",
            "text-\u00e9-\u65e5\u672c-\U0001f469\u200d\U0001f4bb-'quoted'-\\text",
        ),
    ],
    ids=["screen", "osc-bel", "osc-st", "c1", "whitespace-controls", "unicode"],
)
def test_error_values(
    app: typer.Typer,
    command: str,
    prefix: str,
    message: str,
    value: str,
    escaped: str,
    color: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from typer import rich_utils

    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(rich_utils, "FORCE_TERMINAL", color)
    monkeypatch.setattr(rich_utils, "MAX_WIDTH", 3000)
    result = runner.invoke(app, [command, prefix + "input-" + value], color=color)

    assert result.exit_code == 2
    # Remove only generated color styles so other terminal controls cannot hide.
    output = re.sub(r"\x1b\[[0-9;]*m", "", result.stderr)
    assert message in output
    assert prefix + "input-" + escaped in output
    assert re.search(r"[\x00-\x09\x0b-\x1f\x7f-\x9f]", output) is None


def test_unknown_option_preserves_original_value() -> None:
    value = "--input-\x00\x1f\x7f\x80\x9f"
    error = NoSuchOption(value)

    assert error.option_name == value
    assert error.format_message() == r"No such option: --input-\x00\x1f\x7f\x80\x9f"


def test_argument_preserves_original_value() -> None:
    app = typer.Typer(add_completion=False)
    value = "input-\x1b[2J\x1b]52;c;YWJj\x07"

    @app.command()
    def main(value: str) -> None:
        typer.echo(repr(value))

    result = runner.invoke(app, [value])

    assert result.exit_code == 0
    assert result.stdout == repr(value) + "\n"


def test_echo_preserves_terminal_sequences() -> None:
    app = typer.Typer(add_completion=False)
    value = "\x1b[2J\x1b]52;c;YWJj\x07"

    @app.command()
    def main() -> None:
        typer.echo(value)

    result = runner.invoke(app, color=True)

    assert result.exit_code == 0
    assert result.stdout_bytes == value.encode() + b"\n"
