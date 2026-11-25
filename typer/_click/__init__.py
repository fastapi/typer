"""
Code taken and adapted from Click: https://github.com/pallets/click/releases/tag/8.3.1
"""

__lazy_modules__ = {
    "typer._click.core",
    "typer._click.exceptions",
    "typer._click.formatting",
    "typer._click.termui",
    "typer._click.utils",
}

from .core import Command as Command
from .core import Context as Context
from .core import Parameter as Parameter
from .exceptions import ClickException as ClickException
from .formatting import HelpFormatter as HelpFormatter
from .termui import launch as launch
from .utils import echo as echo
