"""
Tests for the Windows console functionality.
Created after vendoring Click to ensure test coverage is back up to 100%.
"""

import ctypes
import io
import sys

import pytest
import typer
from typer.testing import CliRunner

from .utils import needs_windows

pytestmark = needs_windows


if sys.platform == "win32":
    from typer._click import _compat, _winconsole


def _identity_buffer(obj, writable=False):  # noqa: ARG001
    return obj


def _route_console_stream(target_name, wrapper, state=None):
    def patched_windows_stream(stream, encoding, errors):  # noqa: ARG001
        current_target = getattr(sys, target_name)
        if stream is current_target:
            if state is not None and target_name == "stderr":
                state["stderr_wrap_calls"] += 1
            buffer = getattr(stream, "buffer", None)
            return wrapper(buffer) if buffer else None
        return None

    return patched_windows_stream


def _capture_write_console(state):
    def fake_write_console(handle, buffer, units_to_write, units_written_ptr, reserved):  # noqa: ARG001
        state["write_calls"] += 1
        bytes_to_write = units_to_write * 2
        state["written"].extend(buffer[:bytes_to_write])
        units_written_ptr._obj.value = units_to_write
        return 1

    return fake_write_console


def test_winconsole_stdin(monkeypatch):
    runner = CliRunner()
    app = typer.Typer()

    @app.command()
    def read_name(config: typer.FileText = typer.Option(...)) -> None:
        name = config.readline().strip()
        typer.echo(f"Hello {name}")

    utf16_data = bytearray("Rick\r\n".encode("utf-16-le"))
    state = {"pos": 0, "read_calls": 0}

    def fake_read_console(handle, buffer, units_to_read, units_read_ptr, reserved):  # noqa: ARG001
        state["read_calls"] += 1
        max_bytes = units_to_read * 2
        chunk = utf16_data[state["pos"] : state["pos"] + max_bytes]
        if chunk:
            buffer[0 : len(chunk)] = chunk
            state["pos"] += len(chunk)
            units_read_ptr._obj.value = len(chunk) // 2
            return 1

        return 1  # pragma: no cover

    monkeypatch.setattr(_winconsole, "get_buffer", _identity_buffer)
    monkeypatch.setattr(_winconsole, "ReadConsoleW", fake_read_console)
    monkeypatch.setattr(_winconsole, "GetLastError", lambda: 0)
    monkeypatch.setattr(
        _compat,
        "_get_windows_console_stream",
        _route_console_stream("stdin", _winconsole._get_text_stdin),
    )

    result = runner.invoke(app, ["--config", "-"])
    assert result.exit_code == 0, result.output
    assert "Hello Rick" in result.stdout
    assert state["read_calls"] > 0


def test_winconsole_stdout(monkeypatch):
    runner = CliRunner()
    app = typer.Typer()
    state = {"write_calls": 0, "written": bytearray()}

    @app.command()
    def write_message(out: typer.FileTextWrite = typer.Option(...)) -> None:
        out.write("Hello Summer\n")

    monkeypatch.setattr(_winconsole, "get_buffer", _identity_buffer)
    monkeypatch.setattr(_winconsole, "WriteConsoleW", _capture_write_console(state))
    monkeypatch.setattr(_winconsole, "GetLastError", lambda: 0)
    monkeypatch.setattr(
        _compat,
        "_get_windows_console_stream",
        _route_console_stream("stdout", _winconsole._get_text_stdout),
    )

    result = runner.invoke(app, ["--out", "-"])
    assert result.exit_code == 0, result.output
    assert state["write_calls"] > 0
    assert _winconsole._WindowsConsoleWriter(1).isatty() is True
    decoded = state["written"].decode("utf-16-le", errors="ignore")
    assert "Hello Summer\r\n" in decoded


def test_winconsole_stderr(monkeypatch):
    runner = CliRunner()
    app = typer.Typer()
    state = {"write_calls": 0, "written": bytearray(), "stderr_wrap_calls": 0}

    @app.command()
    def main() -> None:
        typer.echo("Ran out of adventure time!", err=True)

    monkeypatch.setattr(_winconsole, "get_buffer", _identity_buffer)
    monkeypatch.setattr(_winconsole, "WriteConsoleW", _capture_write_console(state))
    monkeypatch.setattr(_winconsole, "GetLastError", lambda: 0)
    monkeypatch.setattr(
        _compat,
        "_get_windows_console_stream",
        _route_console_stream("stderr", _winconsole._get_text_stderr, state),
    )

    result = runner.invoke(app)
    assert result.exit_code == 0, result.output
    assert state["stderr_wrap_calls"] > 0
    assert state["write_calls"] > 0
    decoded = state["written"].decode("utf-16-le", errors="ignore")
    assert "Ran out of adventure time!\r\n" in decoded


@pytest.mark.parametrize(
    ("writable", "source", "expected_flags"),
    [
        (True, bytearray(b"python"), 1),  # PyBUF_WRITABLE
        (False, b"python", 0),  # PyBUF_SIMPLE
    ],
)
def test_get_buffer(monkeypatch, writable, source, expected_flags):
    state = {"flags": None, "released": 0}
    if writable:
        backing = (_winconsole.c_char * len(source)).from_buffer(source)
    else:
        backing = (_winconsole.c_char * len(source)).from_buffer_copy(source)
    backing_ptr = _winconsole.c_void_p(ctypes.addressof(backing))

    def fake_object_get_buffer(obj, buf_ref, flags):  # noqa: ARG001
        state["flags"] = flags
        buf = buf_ref._obj
        buf.buf = backing_ptr
        buf.len = len(source)

    def fake_buffer_release(buf_ref):  # noqa: ARG001
        state["released"] += 1

    monkeypatch.setattr(_winconsole, "PyObject_GetBuffer", fake_object_get_buffer)
    monkeypatch.setattr(_winconsole, "PyBuffer_Release", fake_buffer_release)

    probe = source if writable else b"x"
    out = _winconsole.get_buffer(probe, writable=writable)
    if writable:
        # mutate the first byte of "python" to obtain another beloved programming language
        out[0] = b"c"
        assert source == bytearray(b"cython")
    else:
        assert bytes(out[: len(source)]) == source
    assert state["flags"] == expected_flags
    assert state["released"] == 1


def test_isatty():
    assert _winconsole._WindowsConsoleRawIOBase(None).isatty() is True
    assert _winconsole._WindowsConsoleReader(0).isatty() is True
    assert _winconsole._WindowsConsoleReader(1).isatty() is True


def test_console_stream():
    class NamedBytesIO(io.BytesIO):
        name = "fake-buffer"

        def isatty(self):
            return False

    stream = _winconsole.ConsoleStream(
        io.TextIOWrapper(io.BytesIO(), encoding="utf-8"), NamedBytesIO()
    )
    assert stream.isatty() is False
    assert stream.name == "fake-buffer"
    assert "fake-buffer" in repr(stream)
    assert "utf-8" in repr(stream)

    # test writelines
    stream.writelines(["hello", " ", "world"])
    stream._text_stream.flush()
    assert stream._text_stream.buffer.getvalue().decode("utf-8") == "hello world"

    # Cover bytes write path.
    assert stream.write(b"!") == 1
    assert stream.buffer.getvalue().endswith(b"!")


@pytest.mark.parametrize(
    ("error", "msg"),
    [
        (0, "ERROR_SUCCESS"),  # ERROR_SUCCESS
        (8, "ERROR_NOT_ENOUGH_MEMORY"),  # ERROR_NOT_ENOUGH_MEMORY
        (342, "Windows error 342"),
    ],
)
def test_error_message(error, msg):
    writer = _winconsole._WindowsConsoleWriter
    assert writer._get_error_message(error) == msg


def test_is_console():
    assert _winconsole._is_console(object()) is False


def test_get_windows_console_stream_factory_and_buffer_paths(monkeypatch):
    monkeypatch.setattr(_winconsole, "_is_console", lambda f: True)
    monkeypatch.setattr(_winconsole, "get_buffer", object())

    class FakeStream:
        def __init__(self, fd, buffer=None):
            self._fd = fd
            self.buffer = buffer

        def fileno(self):
            return self._fd

    wrapped = {"called": False, "buffer": None}

    def fake_factory(buffer):
        wrapped["called"] = True
        wrapped["buffer"] = buffer
        return "wrapped", buffer

    monkeypatch.setattr(_winconsole, "_stream_factories", {7: fake_factory})

    # Known console stream preconditions pass, but no stream factory for this fd.
    get_stream = _winconsole._get_windows_console_stream
    assert get_stream(FakeStream(99, object()), "utf-16-le", "strict") is None

    # Factory exists, but stream has no usable .buffer.
    assert get_stream(FakeStream(7, None), "utf-16-le", "strict") is None

    # Factory exists and buffer is present, so wrapper result is returned.
    raw_buffer = object()
    out = get_stream(FakeStream(7, raw_buffer), "utf-16-le", "strict")
    assert out == ("wrapped", raw_buffer)
    assert wrapped["called"] is True
    assert wrapped["buffer"] is raw_buffer


def test_windows_console_reader(monkeypatch):
    reader = _winconsole._WindowsConsoleReader(42)

    # Empty input buffer returns early
    assert reader.readinto(bytearray()) == 0

    # Require an even number of bytes
    with pytest.raises(ValueError):
        reader.readinto(bytearray(3))

    def writable_buffer(obj, writable=False):  # noqa: ARG001
        return (ctypes.c_char * len(obj)).from_buffer(obj)

    monkeypatch.setattr(_winconsole, "get_buffer", writable_buffer)

    def patch_console(read_console, error):
        monkeypatch.setattr(_winconsole, "ReadConsoleW", read_console)
        monkeypatch.setattr(_winconsole, "GetLastError", lambda: error)

    def make_read(payload=b"", rv=1, units_read=None):
        def read_console(handle, buffer, units_to_read, units_read_ptr, reserved):  # noqa: ARG001
            bytes_to_copy = min(len(payload), units_to_read * 2)
            if bytes_to_copy:
                buffer[0:bytes_to_copy] = payload[:bytes_to_copy]
            read_units = units_read if units_read is not None else bytes_to_copy // 2
            units_read_ptr._obj.value = read_units
            return rv

        return read_console

    # Normal successful read returns the number of bytes read
    patch_console(make_read(payload=b"A\x00B\x00"), _winconsole.ERROR_SUCCESS)
    assert reader.readinto(bytearray(4)) == 4

    # CTRL+Z (EOF) should be translated into an empty read
    patch_console(
        make_read(payload=_winconsole.EOF + b"\x00", units_read=1),
        _winconsole.ERROR_SUCCESS,
    )
    assert reader.readinto(bytearray(2)) == 0

    # An aborted read should sleep briefly while waiting for KeyboardInterrupt
    sleep_state = {"calls": 0}

    def fake_sleep(seconds):
        sleep_state["calls"] += 1
        assert seconds == 0.1

    monkeypatch.setattr(
        _winconsole, "time", type("FakeTime", (), {"sleep": fake_sleep})
    )
    patch_console(
        make_read(payload=b"Z\x00", units_read=1),
        _winconsole.ERROR_OPERATION_ABORTED,
    )
    assert reader.readinto(bytearray(2)) == 2
    assert sleep_state["calls"] == 1

    # Failed reads propagate a Windows error
    patch_console(make_read(rv=0), _winconsole.ERROR_NOT_ENOUGH_MEMORY)
    with pytest.raises(OSError, match="Windows error"):
        reader.readinto(bytearray(2))
