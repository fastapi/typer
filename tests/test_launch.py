import io
import subprocess
from unittest.mock import patch

import pytest
import typer

from tests.utils import needs_linux, needs_macos, needs_windows

url = "http://example.com"


@pytest.mark.parametrize(
    "system, command",
    [
        ("Darwin", "open"),
        ("Linux", "xdg-open"),
        ("FreeBSD", "xdg-open"),
    ],
)
def test_launch_url_unix(system: str, command: str):
    with (
        patch("platform.system", return_value=system),
        patch("shutil.which", return_value=True),
        patch("subprocess.Popen") as mock_popen,
    ):
        typer.launch(url)

    mock_popen.assert_called_once_with(
        [command, url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def test_launch_url_windows():
    with (
        patch("platform.system", return_value="Windows"),
        patch("webbrowser.open") as mock_webbrowser_open,
    ):
        typer.launch(url)

    mock_webbrowser_open.assert_called_once_with(url)


def test_launch_url_no_xdg_open():
    with (
        patch("platform.system", return_value="Linux"),
        patch("shutil.which", return_value=None),
        patch("webbrowser.open") as mock_webbrowser_open,
    ):
        typer.launch(url)

    mock_webbrowser_open.assert_called_once_with(url)


@pytest.fixture
def allow_dev_null(monkeypatch):
    real_open = open

    def fake_open(path, *args, **kwargs):
        if path == "/dev/null":
            return io.StringIO()
        return real_open(path, *args, **kwargs)  # pragma: no cover

    monkeypatch.setattr("builtins.open", fake_open)


@needs_macos
def test_open_url_macos(monkeypatch, allow_dev_null):
    recorded: list[list[str]] = []

    class Proc:
        def wait(self) -> int:
            return 42

    def fake_popen(args, **kwargs):
        recorded.append(list(args))
        return Proc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    assert typer.launch("/path/to/file", wait=True, locate=True) == 42
    assert recorded[0][:3] == ["open", "-W", "-R"]
    assert recorded[0][-1] == "/path/to/file"


@needs_windows
def test_launch_files_windows(monkeypatch):
    calls: list[list[str]] = []

    def fake_call(args):
        calls.append(list(args))
        return 0

    monkeypatch.setattr(subprocess, "call", fake_call)

    assert typer.launch("C:/Tools/readme.txt", wait=True, locate=False) == 0
    assert typer.launch("file:///C:/tmp/a.txt", wait=False, locate=True) == 0
    assert calls.pop(0) == ["start", "/WAIT", "", "C:/Tools/readme.txt"]
    assert calls.pop(0) == ["explorer", "/select,/C:/tmp/a.txt"]

    monkeypatch.setattr(subprocess, "call", lambda a: (_ for _ in ()).throw(OSError()))
    assert typer.launch("D:/no/such/file.txt", wait=False, locate=False) == 127


@needs_linux
def test_open_url_linux_wait(monkeypatch):
    class Proc:
        def __init__(self, code: int = 0) -> None:
            self._code = code

        def wait(self) -> int:
            return self._code

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: Proc(7))

    assert typer.launch("/file", wait=True, locate=False) == 7


@needs_linux
def test_open_url_linux_locate(monkeypatch):
    recorded: list[list[str]] = []

    class Proc:
        def wait(self) -> int:
            return 0  # pragma: no cover

    def fake_popen(args, **kwargs):
        recorded.append(list(args))
        return Proc()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)

    assert typer.launch("/tmp/sub/file.txt", wait=False, locate=True) == 0
    assert recorded[-1] == ["xdg-open", "/tmp/sub"]
