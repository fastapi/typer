import platform
import shutil
import subprocess


def _is_macos() -> bool:
    return platform.system() == "Darwin"


def _is_linux_or_bsd() -> bool:
    if platform.system() == "Linux":
        return True

    return "BSD" in platform.system()


def open_browser(url: str) -> None:
    """
    Open a web browser to the specified URL.

    This function handles different operating systems separately:
    - On macOS (Darwin), it uses the 'open' command.
    - On Linux and BSD, it uses 'xdg-open' if available.
    - On Windows (and other OSes), it uses the standard webbrowser module.

    The function avoids, when possible, using the webbrowser module on Linux and macOS
    to prevent spammy terminal messages from some browsers (e.g., Chrome).
    """

    if _is_macos():
        subprocess.Popen(
            ["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        return

    has_xdg_open = _is_linux_or_bsd() and shutil.which("xdg-open") is not None

    if has_xdg_open:
        subprocess.Popen(
            ["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        return

    import webbrowser

    webbrowser.open(url)
