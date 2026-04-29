"""
Tests for the termui, echo, and CliRunner isolation functionality.
Created after vendoring Click to ensure test coverage is back up to 100%.
"""

import io
import os
from contextlib import contextmanager
from typing import Literal

import pytest
import typer
from typer._click import _termui_impl, termui
from typer.testing import CliRunner

from tests.utils import needs_windows, skip_if_windows


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


def test_clirunner_getchar(monkeypatch) -> None:
    runner = CliRunner()
    app = typer.Typer()

    @app.command()
    def main() -> None:
        first = termui.getchar(echo=False)
        second = termui.getchar(echo=True)
        typer.echo(f"\nfirst={first};second={second}")

    monkeypatch.setattr(termui, "_getchar", None)
    result = runner.invoke(app, [], input="ab")
    assert result.exit_code == 0, result.output
    assert result.stdout.splitlines() == ["b", "first=a;second=b"]


def test_clirunner_env_none(monkeypatch) -> None:
    runner = CliRunner()
    app = typer.Typer()
    env_key = "TYPER_TEST_ENV_REMOVE"
    monkeypatch.setenv(env_key, "present")

    @app.command()
    def main() -> None:
        typer.echo(f"inside={os.environ.get(env_key)}")

    result = runner.invoke(app, [], env={env_key: None})
    assert result.exit_code == 0, result.output
    assert "inside=None" in result.stdout
    assert os.environ.get(env_key) == "present"


@pytest.mark.parametrize(
    ("runner_exc", "invoke_exc"),
    [
        (False, None),
        (True, False),
    ],
)
def test_clirunner_invoke_catch_exceptions(
    runner_exc: bool, invoke_exc: bool | None
) -> None:
    runner = CliRunner(catch_exceptions=runner_exc)
    app = typer.Typer()

    @app.command()
    def main() -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        runner.invoke(app, [], catch_exceptions=invoke_exc)


@pytest.mark.parametrize(
    ("exit_value", "expected_exit_code", "expected_stdout"),
    [
        (None, 0, ""),
        ("bad-exit", 1, "bad-exit\n"),
    ],
)
def test_clirunner_invoke_system_exit_branches(
    exit_value: object,
    expected_exit_code: int,
    expected_stdout: str,
) -> None:
    runner = CliRunner()
    app = typer.Typer()

    @app.command()
    def main() -> None:
        raise SystemExit(exit_value)

    result = runner.invoke(app, [])
    assert result.exit_code == expected_exit_code
    assert result.stdout == expected_stdout
    if expected_exit_code:
        assert isinstance(result.exception, SystemExit)
    else:
        assert result.exception is None


@needs_windows
def test_termui_impl_windows_raw_terminal():
    with _termui_impl.raw_terminal() as fd:
        assert fd == -1
    with termui.raw_terminal() as fd:
        assert fd == -1


@needs_windows
def test_termui_impl_windows_getchar(monkeypatch):
    monkeypatch.setattr(_termui_impl.msvcrt, "getwch", lambda: "a")
    monkeypatch.setattr(_termui_impl.msvcrt, "getwche", lambda: "b")
    assert _termui_impl.getchar(echo=False) == "a"
    assert _termui_impl.getchar(echo=True) == "b"

    seq_null = iter(["\x00", "K"])
    monkeypatch.setattr(_termui_impl.msvcrt, "getwch", lambda: next(seq_null))
    assert _termui_impl.getchar(echo=False) == "\x00K"

    seq_e0 = iter(["\xe0", "H"])
    monkeypatch.setattr(_termui_impl.msvcrt, "getwch", lambda: next(seq_e0))
    assert _termui_impl.getchar(echo=False) == "\xe0H"

    seq_echo = iter(["\x00", "M"])
    monkeypatch.setattr(_termui_impl.msvcrt, "getwche", lambda: next(seq_echo))
    assert _termui_impl.getchar(echo=True) == "\x00M"

    seq_e0_echo = iter(["\xe0", "Z"])
    monkeypatch.setattr(_termui_impl.msvcrt, "getwche", lambda: next(seq_e0_echo))
    assert _termui_impl.getchar(echo=True) == "\xe0Z"

    monkeypatch.setattr(_termui_impl.msvcrt, "getwch", lambda: "\x03")
    with pytest.raises(KeyboardInterrupt):
        _termui_impl.getchar(echo=False)

    monkeypatch.setattr(_termui_impl.msvcrt, "getwch", lambda: "\x1a")
    with pytest.raises(EOFError):
        _termui_impl.getchar(echo=False)


@skip_if_windows
@pytest.mark.parametrize("use_stdin_tty", [True, False])
def test_termui_impl_posix_raw_terminal(monkeypatch, use_stdin_tty: bool):
    state: dict[str, object] = {}
    flushed: list[None] = []
    fake_tty = None

    if use_stdin_tty:
        expected_fd = 14
        old_termios = "old_settings"
        monkeypatch.setattr(
            _termui_impl, "isatty", lambda s: s is _termui_impl.sys.stdin
        )
        monkeypatch.setattr(_termui_impl.sys.stdin, "fileno", lambda: expected_fd)
    else:
        expected_fd = 27
        old_termios = "old"
        monkeypatch.setattr(
            _termui_impl,
            "isatty",
            lambda s: s is not _termui_impl.sys.stdin,
        )

        class FakeTTY:
            def __init__(self) -> None:
                self.closed = False

            def fileno(self) -> int:
                return expected_fd

            def close(self) -> None:
                self.closed = True

        fake_tty = FakeTTY()
        real_open = open

        def fake_open(path, *args, **kwargs):
            if path == "/dev/tty":
                return fake_tty
            return real_open(path, *args, **kwargs)  # pragma: no cover

        monkeypatch.setattr("builtins.open", fake_open)

    def tcgetattr(fd: int) -> str:
        state["tcgetattr_fd"] = fd
        return old_termios

    def setraw(fd: int) -> None:
        state["setraw_fd"] = fd

    def tcsetattr(fd: int, when: int, old: str) -> None:
        state["tcsetattr"] = (fd, when, old)

    monkeypatch.setattr(_termui_impl.termios, "tcgetattr", tcgetattr)
    monkeypatch.setattr(_termui_impl.tty, "setraw", setraw)
    monkeypatch.setattr(_termui_impl.termios, "tcsetattr", tcsetattr)
    monkeypatch.setattr(
        _termui_impl.sys.stdout, "flush", lambda *a, **k: flushed.append(None)
    )

    with _termui_impl.raw_terminal() as fd:
        assert fd == expected_fd

    assert state["tcgetattr_fd"] == expected_fd
    assert state["setraw_fd"] == expected_fd
    assert state["tcsetattr"] == (
        expected_fd,
        _termui_impl.termios.TCSADRAIN,
        old_termios,
    )
    assert flushed == [None]
    if fake_tty is not None:
        assert fake_tty.closed is True


@skip_if_windows
def test_termui_impl_posix_getchar(monkeypatch):
    @contextmanager
    def fake_raw():
        yield 7

    monkeypatch.setattr(_termui_impl, "raw_terminal", fake_raw)
    monkeypatch.setattr(_termui_impl.os, "read", lambda fd, n: b"q")
    monkeypatch.setattr(_termui_impl, "get_best_encoding", lambda stdin: "utf-8")
    monkeypatch.setattr(_termui_impl, "isatty", lambda f: f is _termui_impl.sys.stdout)
    written: list[str] = []
    monkeypatch.setattr(_termui_impl.sys.stdout, "write", lambda s: written.append(s))

    assert _termui_impl.getchar(echo=True) == "q"
    assert written == ["q"]


@skip_if_windows
def test_termui_impl_posix_getchar_eof(monkeypatch):
    @contextmanager
    def fake_raw():
        yield 5

    monkeypatch.setattr(_termui_impl, "raw_terminal", fake_raw)
    monkeypatch.setattr(_termui_impl.os, "read", lambda fd, n: b"\x04")
    monkeypatch.setattr(_termui_impl, "get_best_encoding", lambda stdin: "utf-8")
    monkeypatch.setattr(_termui_impl, "isatty", lambda f: False)

    with pytest.raises(EOFError):
        _termui_impl.getchar(echo=False)


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
    assert (
        "accept=True;name=Ada;flavor=a;city=London;config=custom.ini;pass_len=6"
        in result.stdout
    )
    assert "(a, b): " in result.stdout
    assert "[demo.txt]: " in result.stdout


def test_hidden_prompt_func(monkeypatch):
    monkeypatch.setattr("getpass.getpass", lambda prompt: "secret")
    assert termui.hidden_prompt_func("Password: ") == "secret"


def test_echo_stdout_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("sys.stdout", None)
    typer.echo("ignored")


def test_echo_stringifies() -> None:
    stream = io.StringIO()
    typer.echo(123, file=stream, nl=False)
    assert stream.getvalue() == "123"


def test_echo_bytes() -> None:
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="utf-8")
    typer.echo(b"abc", file=stream, nl=True)
    assert buffer.getvalue() == b"abc\n"


def test_echo_empty_output() -> None:
    class FlushTrackingTextStream(io.StringIO):
        def __init__(self) -> None:
            super().__init__()
            self.flush_count = 0

        def flush(self) -> None:
            self.flush_count += 1
            super().flush()

        def write(self, s: str) -> int:
            raise AssertionError("Empty output")  # pragma: no cover

    stream = FlushTrackingTextStream()
    typer.echo("", file=stream, nl=False)
    assert stream.flush_count == 1


@needs_windows
def test_echo_windows_color_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class TtyStream(io.StringIO):
        def isatty(self) -> bool:
            return True

    stream = TtyStream()
    monkeypatch.setattr("typer._click.utils.auto_wrap_for_ansi", None)
    typer.echo("\x1b[31mred\x1b[0m", file=stream, nl=False, color=None)
    assert stream.getvalue() == "red"


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
