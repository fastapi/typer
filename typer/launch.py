import platform
import shutil
import subprocess

from click import launch as click_launch


def _is_macos() -> bool:
    return platform.system() == "Darwin"


def _is_linux_or_bsd() -> bool:
    if platform.system() == "Linux":
        return True

    return "BSD" in platform.system()


def launch(url: str, wait: bool = False, locate: bool = False) -> int:
    """This function launches the given URL (or filename) in the default
    viewer application for this file type.  If this is an executable, it
    might launch the executable in a new session.  The return value is
    the exit code of the launched application.  Usually, ``0`` indicates
    success.

    This function handles url in different operating systems separately:
    - On macOS (Darwin), it uses the 'open' command.
    - On Linux and BSD, it uses 'xdg-open' if available.
    - On Windows (and other OSes), it uses the standard webbrowser module.

    The function avoids, when possible, using the webbrowser module on Linux and macOS
    to prevent spammy terminal messages from some browsers (e.g., Chrome).

    Examples::

        typer.launch('https://click.palletsprojects.com/')
        typer.launch('/my/downloaded/file', locate=True)

    :param url: URL or filename of the thing to launch.
    :param wait: Wait for the program to exit before returning. This
        only works if the launched program blocks. In particular,
        ``xdg-open`` on Linux does not block.
    :param locate: if this is set to `True` then instead of launching the
                   application associated with the URL it will attempt to
                   launch a file manager with the file located.  This
                   might have weird effects if the URL does not point to
                   the filesystem.
    """

    if url.startswith("http://") or url.startswith("https://"):
        if _is_macos():
            return subprocess.Popen(
                ["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ).wait()

        has_xdg_open = _is_linux_or_bsd() and shutil.which("xdg-open") is not None

        if has_xdg_open:
            return subprocess.Popen(
                ["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            ).wait()

        import webbrowser

        webbrowser.open(url)

        return 0

    else:
        return click_launch(url)
