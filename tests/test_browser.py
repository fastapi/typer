import subprocess
from unittest.mock import patch

import pytest
import typer

url = "http://example.com"


@pytest.mark.parametrize(
    "system, command",
    [
        ("Darwin", "open"),
        ("Linux", "xdg-open"),
        ("FreeBSD", "xdg-open"),
    ],
)
def test_open_browser_unix(system: str, command: str):
    with patch("platform.system", return_value=system), patch(
        "shutil.which", return_value=True
    ), patch("subprocess.Popen") as mock_popen:
        typer.open_browser(url)

    mock_popen.assert_called_once_with(
        [command, url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def test_open_browser_windows():
    with patch("platform.system", return_value="Windows"), patch(
        "webbrowser.open"
    ) as mock_webbrowser_open:
        typer.open_browser(url)

    mock_webbrowser_open.assert_called_once_with(url)


def test_open_browser_no_xdg_open():
    with patch("platform.system", return_value="Linux"), patch(
        "shutil.which", return_value=None
    ), patch("webbrowser.open") as mock_webbrowser_open:
        typer.open_browser(url)

    mock_webbrowser_open.assert_called_once_with(url)
