import sys
from typing import Union

import click

if sys.version_info >= (3, 8):
    from typing import get_args as _get_args
    from typing import get_origin as _get_origin
elif sys.version_info >= (3, 7):
    from typing_extensions import get_args as _get_args
    from typing_extensions import get_origin as _get_origin
else:
    # These methods do not handle all the same details as the imported ones.
    # However on Python 3.6 they should be sufficient.
    # typer <= 0.7.0 used this implementation on all Python versions.

    def _get_origin(arg):  # pragma: no cover
        return getattr(arg, "__origin__", None)

    def _get_args(arg):  # pragma: no cover
        return getattr(arg, "__args__", None)


# Assigning variables to mark them as exported with mypy
get_origin = _get_origin
get_args = _get_args

if sys.version_info >= (3, 10):
    from types import UnionType

    UNION_TYPES = (UnionType, Union)
else:
    UNION_TYPES = (Union,)


def _get_click_major() -> int:
    return int(click.__version__.split(".")[0])
