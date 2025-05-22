import functools
from typing import Any, Callable, TypeVar

import click

F = TypeVar("F", bound=Callable[..., Any])


# TODO: remove this when dropping support for Click < 8.2
def add_ctx_arg(f: F) -> F:
    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "ctx" not in kwargs:
            kwargs["ctx"] = click.get_current_context(silent=True)

        return f(*args, **kwargs)

    return wrapper  # type: ignore[return-value]
