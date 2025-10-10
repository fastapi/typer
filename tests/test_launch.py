import subprocess
from unittest.mock import patch

import pytest
import typer

url = "http://example.com"


@pytest.mark.parametrize(
    "system, sys_platform, command",
    [
        ("Darwin", "darwin", "open"),
        ("Linux", "linux", "xdg-open"),
        ("FreeBSD", "freebsd8", "xdg-open"),
    ],
)
def test_launch_url_unix(system: str, sys_platform: str, command: str):
    with patch("platform.system", return_value=system), patch(
        "sys.platform", sys_platform
    ), patch("shutil.which", return_value=True), patch(
        "subprocess.Popen"
    ) as mock_popen:
        typer.launch(url)

    mock_popen.assert_called_once_with(
        [command, url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def test_launch_url_windows():
    with patch("sys.platform", "windows"), patch(
        "webbrowser.open"
    ) as mock_webbrowser_open:
        typer.launch(url)

    mock_webbrowser_open.assert_called_once_with(url)


def test_launch_url_no_xdg_open():
    with patch("sys.platform", "linux"), patch(
        "shutil.which", return_value=None
    ), patch("webbrowser.open") as mock_webbrowser_open:
        typer.launch(url)

    mock_webbrowser_open.assert_called_once_with(url)


def test_calls_original_launch_when_not_passing_urls():
    with patch("typer.main.click.launch", return_value=0) as launch_mock:
        typer.launch("not a url")

    launch_mock.assert_called_once_with("not a url")
