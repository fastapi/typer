import io
from contextlib import contextmanager
from typing import Literal

import pytest
import typer
from typer._click import _termui_impl, termui
from typer.testing import CliRunner


def test_raw_terminal(monkeypatch):
    runner = CliRunner()
    app = typer.Typer()
    state = {"entered": 0, "exited": 0}

    @contextmanager
    def fake_raw_terminal():
        state["entered"] += 1
        try:
            yield 42
        finally:
            state["exited"] += 1

    monkeypatch.setattr(_termui_impl, "raw_terminal", fake_raw_terminal)

    @app.command()
    def main():
        with termui.raw_terminal() as fd:
            typer.echo(f"fd={fd}")

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    assert "fd=42" in result.stdout
    assert state["entered"] == 1
    assert state["exited"] == 1


def test_getchar(monkeypatch):
    # Cached path: call the existing _getchar directly.
    cached_state = {"echo": None}

    def cached_getchar(echo: bool) -> str:
        cached_state["echo"] = echo
        return "x"

    monkeypatch.setattr(termui, "_getchar", cached_getchar)
    assert termui.getchar(echo=True) == "x"
    assert cached_state["echo"] is True

    # Lazy-load path: _getchar is None, so import/cache _termui_impl.getchar.
    lazy_state = {"calls": 0}

    def lazy_getchar(echo: bool) -> str:
        lazy_state["calls"] += 1
        return "y" if not echo else "z"

    monkeypatch.setattr(termui, "_getchar", None)
    monkeypatch.setattr(_termui_impl, "getchar", lazy_getchar)

    assert termui.getchar(echo=False) == "y"
    assert termui._getchar is lazy_getchar
    assert termui.getchar(echo=True) == "z"
    assert lazy_state["calls"] == 2


def test_prompt():
    runner = CliRunner()
    app = typer.Typer()
    fake_file = io.StringIO("data")
    fake_file.name = "demo.txt"

    @app.command()
    def main(
        accept: bool = typer.Option(True, prompt=True),
        name: str = typer.Option(..., prompt=True),
        flavor: Literal["a", "b"] = typer.Option(..., prompt=True),
        city: str = typer.Option("London", prompt=True),
        config: str = typer.Option(fake_file, prompt=True),
        password: str = typer.Option(
            ...,
            prompt=True,
            hide_input=True,
            confirmation_prompt=True,
        ),
    ):
        typer.echo(
            f"accept={accept};name={name};flavor={flavor};city={city};config={config};pass_len={len(password)}"
        )

    result = runner.invoke(app, [], input="\nAda\na\n\ncustom.ini\nsecret\nsecret\n")
    assert result.exit_code == 0, result.output
    assert "accept=True;name=Ada;flavor=a;city=London;config=custom.ini;pass_len=6" in result.stdout
    assert "(a, b): " in result.stdout
    assert "[demo.txt]: " in result.stdout


def test_hidden_prompt_func(monkeypatch):
    monkeypatch.setattr("getpass.getpass", lambda prompt: "secret")
    assert termui.hidden_prompt_func("Password: ") == "secret"


@pytest.mark.parametrize(
    ("flag", "true_code", "false_code"),
    [
        ("bold", "\x1b[1m", "\x1b[22m"),
        ("dim", "\x1b[2m", "\x1b[22m"),
        ("underline", "\x1b[4m", "\x1b[24m"),
        ("overline", "\x1b[53m", "\x1b[55m"),
        ("italic", "\x1b[3m", "\x1b[23m"),
        ("blink", "\x1b[5m", "\x1b[25m"),
        ("reverse", "\x1b[7m", "\x1b[27m"),
        ("strikethrough", "\x1b[9m", "\x1b[29m"),
    ],
)
def test_style(flag, true_code, false_code):
    runner = CliRunner()
    app = typer.Typer()

    @app.command()
    def main():
        # testing an int and a str on purpose
        typer.echo("TRUE=" + typer.style("42", **{flag: True}), color=True)
        typer.echo("FALSE=" + typer.style(666, **{flag: False}), color=True)

    result = runner.invoke(app, [])
    assert result.exit_code == 0, result.output
    lines = [line for line in result.stdout.splitlines() if line]
    true_line = next(line for line in lines if line.startswith("TRUE="))
    false_line = next(line for line in lines if line.startswith("FALSE="))
    assert "42" in true_line
    assert "666" in false_line

    assert true_code in true_line
    assert true_code not in false_line
    assert false_code in false_line
    assert false_code not in true_line


def test_style_color():
    fg_int = typer.style("x", fg=123)
    assert "\x1b[38;5;123m" in fg_int

    bg_list = typer.style("x", bg=[1, 2, 3])
    assert "\x1b[48;2;1;2;3m" in bg_list

    with pytest.raises(TypeError, match="Unknown color"):
        typer.style("x", fg="not-a-color")

    with pytest.raises(TypeError, match="Unknown color"):
        typer.style("x", bg="not-a-color")


def test_termui_launch(monkeypatch):
    captured = {}

    def fake_open_url(url, wait=False, locate=False):
        captured["url"] = url
        captured["wait"] = wait
        captured["locate"] = locate
        return 7

    monkeypatch.setattr(_termui_impl, "open_url", fake_open_url)
    rv = termui.launch("https://example.com", wait=True, locate=True)
    assert rv == 7
    assert captured == {
        "url": "https://example.com",
        "wait": True,
        "locate": True,
    }
