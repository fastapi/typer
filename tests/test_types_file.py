import builtins
import subprocess
import sys
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path

import pytest
import typer
from typer._click._compat import get_best_encoding, should_strip_ansi
from typer._click.testing import make_input_stream
from typer._click.utils import PacifyFlushWrapper
from typer.testing import CliRunner

from tests.utils import needs_linux, needs_windows

app = typer.Typer()


@app.command()
def read_text(file_in: typer.FileText = typer.Option(..., lazy=True)):
    data = file_in.read()
    typer.echo(f"text-len={len(data)}")


@app.command()
def write_text(file_out: typer.FileTextWrite = typer.Option(..., lazy=None)):
    file_out.write("This is a single line\n")
    typer.echo("1 line written")


@app.command()
def write_lazy(file_out: typer.FileTextWrite = typer.Option(..., lazy=True)):
    file_out.write("This is a single lazy line\n")
    typer.echo("1 line written")


@app.command()
def probe_lazy_file_behaviors(
    file_in: typer.FileText = typer.Option(..., lazy=True),
    file_out: typer.FileTextWrite = typer.Option(..., lazy=True),
):
    typer.echo(f"repr-before={repr(file_out)}")
    file_out.write("repr-opened\n")
    typer.echo(f"repr-after={repr(file_out)}")
    with file_in as stream:
        typer.echo(f"context-len={len(stream.read())}")
        stream.seek(0)
        first_line = next(iter(stream), "")
        typer.echo(f"first-line={first_line.rstrip()}")


@app.command()
def write_binary(file_out: typer.FileBinaryWrite = typer.Option(...)):
    file_out.write(b"binary-written\n")


@app.command()
def write_binary_stderr():
    stream = typer.get_binary_stream("stderr")
    stream.write(b"binary-stderr\n")
    stream.flush()


@app.command()
def read_binary(file_in: typer.FileBinaryRead = typer.Option(...)):
    data = file_in.read()
    typer.echo(f"binary-len={len(data)}")


runner = CliRunner()


def test_text_stdin_dash() -> None:
    result = runner.invoke(app, ["read-text", "--file-in=-"], input="hello\n")
    assert result.exit_code == 0
    assert "text-len=6" in result.output


def test_lazy_file(tmp_path: Path) -> None:
    # dash: written to stdout
    result = runner.invoke(app, ["write-text", "--file-out=-"])
    assert result.exit_code == 0
    assert "This is a single line" in result.output
    assert "1 line written" in result.output

    # lazy + file
    file_path = tmp_path / "example.txt"
    result = runner.invoke(app, ["write-lazy", f"--file-out={file_path}"])
    assert result.exit_code == 0
    assert "This is a single lazy line" not in result.output
    assert "1 line written" in result.output
    assert file_path.exists()
    assert file_path.read_text() == "This is a single lazy line\n"

    # lazy probe: unopened/opened repr, context manager, and iteration.
    result = runner.invoke(
        app,
        [
            "probe-lazy-file-behaviors",
            f"--file-in={file_path}",
            f"--file-out={tmp_path / 'repr-opened.txt'}",
        ],
    )
    assert result.exit_code == 0
    assert "repr-before=<unopened file" in result.output
    assert "repr-after=<unopened file" not in result.output
    assert "repr-opened.txt" in result.output
    assert "context-len=27" in result.output
    assert "first-line=This is a single lazy line" in result.output

    # lazy + dash: written to stdout (lazy setting is pretty much ignored)
    result = runner.invoke(app, ["write-lazy", "--file-out=-"])
    assert result.exit_code == 0
    assert "This is a single lazy line" in result.output
    assert "1 line written" in result.output


def test_filelike_conversion() -> None:
    stream = StringIO()
    result = runner.invoke(
        app, ["write-text"], default_map={"write-text": {"file_out": stream}}
    )
    assert result.exit_code == 0
    assert "1 line written" in result.output
    assert stream.getvalue() == "This is a single line\n"


def test_input_stream() -> None:
    binary_stream = BytesIO(b"hello")
    converted = make_input_stream(binary_stream, charset="utf-8")
    assert converted is binary_stream

    text_stream = TextIOWrapper(BytesIO(b"hello"), encoding="utf-8")
    converted = make_input_stream(text_stream, charset="utf-8")
    assert converted is text_stream.buffer


def test_binary_dash() -> None:
    result = runner.invoke(app, ["write-binary", "--file-out=-"])
    assert result.exit_code == 0
    assert result.stdout_bytes == b"binary-written\n"

    result = runner.invoke(
        app, ["read-binary", "--file-in=-"], input=b"\x00\x01\x02abc"
    )
    assert result.exit_code == 0
    assert "binary-len=6" in result.output


def test_binary_stderr() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tests.test_types_file import app; app()",
            "write-binary-stderr",
        ],
        capture_output=True,
    )
    assert result.returncode == 0
    assert result.stderr == b"binary-stderr\n"


@pytest.mark.parametrize(
    ("errors_arg", "expected_errors"),
    [
        (None, "replace"),
        ("strict", "strict"),
    ],
)
def test_get_text_stream_errors(
    monkeypatch,
    errors_arg: str | None,
    expected_errors: str,
) -> None:
    class BinaryStdout(BytesIO):
        pass

    binary_stdout = BinaryStdout()
    monkeypatch.setattr(sys, "stdout", binary_stdout)

    text_stream = typer.get_text_stream("stdout", encoding=None, errors=errors_arg)
    text_stream.write("stream-text")
    text_stream.flush()

    assert text_stream.errors == expected_errors
    assert text_stream.writable() is True
    assert binary_stdout.getvalue() == b"stream-text"


def test_get_best_encoding() -> None:
    """Test that ASCII is being transformed into UTF-8"""

    class AsciiStream:
        encoding = "ascii"

    class Utf8Stream:
        encoding = "utf-8"

    class UnknownStream:
        encoding = "unknown"

    assert get_best_encoding(AsciiStream()) == "utf-8"
    assert get_best_encoding(Utf8Stream()) == "utf-8"
    assert get_best_encoding(UnknownStream()) == "unknown"


def test_pacify_flush_wrapper() -> None:
    class Wrapped:
        def __init__(self) -> None:
            self.name = "wrapped-stream"

        def flush(self) -> None:
            return None  # pragma: no cover

    wrapped = PacifyFlushWrapper(Wrapped())
    assert wrapped.name == "wrapped-stream"


def test_text_stream_isatty(monkeypatch) -> None:
    class BinaryStdout(BytesIO):
        def isatty(self) -> bool:
            return True

    binary_stdout = BinaryStdout()
    monkeypatch.setattr(sys, "stdout", binary_stdout)
    text_stream = typer.get_text_stream("stdout", encoding="utf-8", errors=None)
    assert text_stream.isatty() is True


def test_text_stream_buffer_read1(monkeypatch) -> None:
    class BinaryStdinNoRead1:
        def __init__(self, data: bytes) -> None:
            self._data = data
            self._pos = 0

        def read(self, size: int = -1) -> bytes:
            if size < 0:
                size = len(self._data) - self._pos  # pragma: no cover
            chunk = self._data[self._pos : self._pos + size]
            self._pos += len(chunk)
            return chunk

    binary_stdin = BinaryStdinNoRead1(b"hello")
    monkeypatch.setattr(sys, "stdin", binary_stdin)
    text_stream = typer.get_text_stream("stdin", encoding="utf-8", errors=None)
    assert text_stream._stream.read1(4) == b"hell"


def test_binary_stream(monkeypatch) -> None:
    binary_stdin = BytesIO(b"hello")
    binary_stdout = BytesIO()
    monkeypatch.setattr(sys, "stdin", binary_stdin)
    monkeypatch.setattr(sys, "stdout", binary_stdout)

    assert typer.get_binary_stream("stdin") is binary_stdin
    assert typer.get_binary_stream("stdout") is binary_stdout


def test_binary_stream_raises(monkeypatch) -> None:
    class TextOnlyStdin:
        def read(self, n: int = -1) -> str:
            return "hello"

    monkeypatch.setattr(sys, "stdin", TextOnlyStdin())
    with pytest.raises(RuntimeError, match="Was not able to determine binary stream"):
        typer.get_binary_stream("stdin")


def test_stream_unknown() -> None:
    with pytest.raises(TypeError, match="Unknown standard stream 'Plumbus'"):
        typer.get_binary_stream("Plumbus")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="Unknown standard stream 'Fleeb'"):
        typer.get_text_stream("Fleeb")  # type: ignore[arg-type]


def test_format_filename() -> None:
    filename = b"folder/subdir/demo.txt"
    assert typer.format_filename(filename, shorten=True) == "demo.txt"


def test_file_error(monkeypatch, tmp_path: Path) -> None:
    file_path = tmp_path / "cannot-open.txt"
    real_open = builtins.open

    def fake_open(path, *args, **kwargs):
        if Path(path) == file_path:
            raise OSError()
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)
    result = runner.invoke(app, ["write-text", f"--file-out={file_path}"])
    assert result.exit_code == 1
    assert "Could not open file" in result.output
    assert "cannot-open.txt" in result.output
    assert "unknown error" in result.output


@needs_windows
def test_app_dir_windows_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.setattr("os.path.expanduser", lambda _path: r"C:\Users\Tester")

    assert typer.get_app_dir("My App", roaming=True) == r"C:\Users\Tester\My App"


@needs_linux
def test_app_dir_force_posix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("os.path.expanduser", lambda _path: "/home/tester/.my-app")

    assert typer.get_app_dir("My App", force_posix=True) == "/home/tester/.my-app"


def test_text_stream_binary_buffer(monkeypatch) -> None:
    class TextStdinWithBinaryBuffer:
        def __init__(self, data: bytes) -> None:
            self.buffer = BytesIO(data)
            self.encoding = "latin-1"

        def read(self, n: int = -1) -> str:
            raise OSError("text stream is not readable directly")

    class TextStdoutWithBinaryBuffer:
        def __init__(self) -> None:
            self.buffer = BytesIO()
            self.encoding = "latin-1"

        def write(self, s: str) -> int:
            raise OSError("text stream is not writable directly")

    stdin = TextStdinWithBinaryBuffer(b"hello")
    stdout = TextStdoutWithBinaryBuffer()

    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)

    text_stdin = typer.get_text_stream("stdin", encoding="utf-8", errors=None)
    text_stdout = typer.get_text_stream("stdout", encoding="utf-8", errors=None)

    assert text_stdin.read() == "hello"
    text_stdout.write("ok")
    text_stdout.flush()
    assert stdout.buffer.getvalue() == b"ok"


def test_text_stream_binary_stream(monkeypatch) -> None:
    binary_stdout = BytesIO()
    monkeypatch.setattr(sys, "stdout", binary_stdout)
    text_stream = typer.get_text_stream("stdout", encoding="utf-8", errors=None)
    text_stream.write("ok")
    text_stream.flush()
    assert binary_stdout.getvalue() == b"ok"


def test_text_stream_stdout_no_binary(
    monkeypatch,
) -> None:
    class TextStdoutNoBinaryFallback:
        encoding = "utf-8"
        errors = "strict"

        def write(self, s: str) -> int:
            if isinstance(s, bytes):
                raise TypeError("bytes not supported")
            return len(s)

    stdout = TextStdoutNoBinaryFallback()
    monkeypatch.setattr(sys, "stdout", stdout)
    text_stream = typer.get_text_stream("stdout", encoding="utf-8", errors="replace")
    assert text_stream is stdout


def test_jupyter_wrapped_stream(monkeypatch) -> None:
    class JupyterLikeStdout(BytesIO):
        __module__ = "ipykernel.iostream"

        def isatty(self) -> bool:
            return False

    binary_stdout = JupyterLikeStdout()
    monkeypatch.setattr(sys, "stdout", binary_stdout)
    text_stream = typer.get_text_stream("stdout", encoding="utf-8", errors=None)
    assert should_strip_ansi(text_stream, color=None) is False


def test_should_strip_ansi(monkeypatch) -> None:
    class NonTtyStdin(BytesIO):
        def isatty(self) -> bool:
            return False

    stdin = NonTtyStdin()
    monkeypatch.setattr(sys, "stdin", stdin)
    assert should_strip_ansi(stream=None, color=None) is True
    assert should_strip_ansi(stream=None, color=True) is False
    assert should_strip_ansi(stream=None, color=False) is True
