import subprocess
import sys
from io import BytesIO, StringIO
from pathlib import Path

import pytest
import typer
from typer._click._compat import get_best_encoding
from typer.testing import CliRunner

app = typer.Typer()


@app.command()
def read_text(file_in: typer.FileText = typer.Option(...)):
    data = file_in.read()
    typer.echo(f"text-len={len(data)}")


@app.command()
def write_text(file_out: typer.FileTextWrite = typer.Option(..., lazy=None)):
    file_out.write("This is a single line\n")
    print("1 line written")


@app.command()
def write_lazy(file_out: typer.FileTextWrite = typer.Option(..., lazy=True)):
    file_out.write("This is a single line\n")
    print("1 line written")


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


def test_lazy_file() -> None:
    # dash: written to stdout
    result = runner.invoke(app, ["write-text", "--file-out=-"])
    assert result.exit_code == 0
    assert "This is a single line" in result.output
    assert "1 line written" in result.output

    # lazy + file
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["write-lazy", "--file-out=example.txt"])
        assert result.exit_code == 0
        assert "This is a single line" not in result.output
        assert "1 line written" in result.output
        # test that the file is created
        file_path = Path("example.txt")
        assert file_path.exists()
        with file_path.open("r") as f:
            assert f.read() == "This is a single line\n"

    # lazy + dash: written to stdout (lazy setting is pretty much ignored)
    result = runner.invoke(app, ["write-lazy", "--file-out=-"])
    assert result.exit_code == 0
    assert "This is a single line" in result.output
    assert "1 line written" in result.output


def test_filelike_conversion() -> None:
    stream = StringIO()
    result = runner.invoke(
        app, ["write-text"], default_map={"write-text": {"file_out": stream}}
    )
    assert result.exit_code == 0
    assert "1 line written" in result.output
    assert stream.getvalue() == "This is a single line\n"


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


def test_get_text_stream_binary_stdin(monkeypatch) -> None:
    class BinaryStdin(BytesIO):
        def readable(self) -> bool:
            return False

        def writable(self) -> bool:
            return False

    binary_stdin = BinaryStdin(b"hello")
    monkeypatch.setattr(sys, "stdin", binary_stdin)

    text_stream = typer.get_text_stream("stdin", encoding=None, errors=None)

    assert text_stream.read() == "hello"
    assert text_stream.readable() is True  # forced to True
    assert text_stream.writable() is False


def test_get_text_stream_binary_stdout(monkeypatch) -> None:
    class BinaryStdout(BytesIO):
        def writable(self) -> bool:
            return False

        def seekable(self) -> bool:
            return False

        def readable(self) -> bool:
            return False

        def isatty(self) -> bool:
            return True

    binary_stdout = BinaryStdout()
    monkeypatch.setattr(sys, "stdout", binary_stdout)

    text_stream = typer.get_text_stream("stdout", encoding=None, errors=None)

    assert text_stream.readable() is False
    assert text_stream.writable() is True  # forced to True
    assert text_stream.seekable() is False
    assert text_stream.isatty() is True
    text_stream.write("ok")
    text_stream.flush()
    assert binary_stdout.getvalue() == b"ok"


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
