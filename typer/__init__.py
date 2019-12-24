"""Typer, an intuitive CLI library based on optional type hints"""

__version__ = "0.0.1"

from .main import Typer, run  # noqa
from .params import Option, Argument  # noqa
from .models import Context, TextFile, BinaryFileRead, BinaryFileWrite  # noqa

# Utilities
from click.utils import (  # noqa
    echo,
    get_binary_stream,
    get_text_stream,
    open_file,
    format_filename,
    get_app_dir,
    get_os_args,
)

# Terminal functions
from click.termui import (  # noqa
    prompt,
    confirm,
    get_terminal_size,
    echo_via_pager,
    progressbar,
    clear,
    style,
    unstyle,
    secho,
    edit,
    launch,
    getchar,
    pause,
)

from click.exceptions import (  # noqa
    ClickException,
    UsageError,
    BadParameter,
    FileError,
    Abort,
    NoSuchOption,
    BadOptionUsage,
    BadArgumentUsage,
    MissingParameter,
)
