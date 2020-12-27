import asyncio
import inspect
import sys
from typing import Any, Awaitable, Callable, Dict, TypeVar, get_type_hints

from .models import ParamMeta

_T = TypeVar("_T")


def get_params_from_function(func: Callable[..., Any]) -> Dict[str, ParamMeta]:
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    params = {}
    for param in signature.parameters.values():
        annotation = param.annotation
        if param.name in type_hints:
            annotation = type_hints[param.name]
        params[param.name] = ParamMeta(
            name=param.name, default=param.default, annotation=annotation
        )
    return params


def aio_run(aw: Awaitable[_T]) -> _T:
    """Run an async/awaitable function (Polyfill asyncio.run)
    Examples:
    >>> async def add(a, b):
    ...     return a + b
    ...
    >>> aio.run(add(1, 4))
    5
    """
    if sys.version_info >= (3, 7):
        return asyncio.run(aw)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(aw)
    finally:
        loop.close()
        asyncio.set_event_loop(None)


def is_async(obj: Callable[..., Any]) -> bool:
    """Return True if function/obj is is async/awaitable"""
    return asyncio.iscoroutinefunction(obj) or asyncio.iscoroutine(obj)
