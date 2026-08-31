from threading import local
from typing import TYPE_CHECKING, Literal, Union, cast, overload

if TYPE_CHECKING:
    from .core import Context

_local = local()


@overload
def get_current_context(silent: Literal[False] = False) -> "Context": ...


@overload
def get_current_context(silent: bool = ...) -> Union["Context", None]: ...


def get_current_context(silent: bool = False) -> Union["Context", None]:
    """Returns the current click context.  This can be used as a way to
    access the current context object from anywhere.  This is a more implicit
    alternative to the `pass_context` decorator.  This function is
    primarily useful for helpers such as `echo` which might be
    interested in changing its behavior based on the current context.

    To push the current context, `Context.scope` can be used.
    """
    try:
        return cast("Context", _local.stack[-1])
    except (AttributeError, IndexError) as e:
        if not silent:
            raise RuntimeError(
                "There is no active click context."
            ) from e  # pragma: no cover

    return None


def push_context(ctx: "Context") -> None:
    """Pushes a new context to the current stack."""
    _local.__dict__.setdefault("stack", []).append(ctx)


def pop_context() -> None:
    """Removes the top level from the stack."""
    _local.stack.pop()


def resolve_color_default(color: bool | None = None) -> bool | None:
    """Internal helper to get the default value of the color flag.  If a
    value is passed it's returned unchanged, otherwise it's looked up from
    the current context.
    """
    if color is not None:
        return color

    ctx = get_current_context(silent=True)

    if ctx is not None:
        return ctx.color

    return None
