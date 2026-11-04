# Adapted from pydantic 1.9.2
# mypy: ignore-errors

import numbers
import types
from collections.abc import Callable
from typing import (
    Annotated,
    Any,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)


def is_union(tp: type[Any] | None) -> bool:
    return tp is Union or tp is types.UnionType  # noqa: E721


__all__ = (
    "NoneType",
    "is_none_type",
    "is_callable_type",
    "is_literal_type",
    "all_literal_values",
    "is_number_type",
    "is_union",
    "Annotated",
    "Literal",
    "get_args",
    "get_origin",
    "get_type_hints",
)


NoneType = None.__class__


NONE_TYPES: tuple[Any, Any, Any] = (None, NoneType, Literal[None])


def is_none_type(type_: Any) -> bool:
    for none_type in NONE_TYPES:
        if type_ is none_type:
            return True
    return False


def is_callable_type(type_: type[Any]) -> bool:
    return type_ is Callable or get_origin(type_) is Callable


def is_number_type(type_: Any) -> bool:
    return (
        isinstance(type_, type)
        and type_ is not bool
        and type_ is not complex
        and issubclass(type_, numbers.Number)
    )


def is_literal_type(type_: type[Any]) -> bool:
    return get_origin(type_) is Literal


def literal_values(type_: type[Any]) -> tuple[Any, ...]:
    return get_args(type_)


def all_literal_values(type_: type[Any]) -> tuple[Any, ...]:
    """
    This method is used to retrieve all Literal values as
    Literal can be used recursively (see https://www.python.org/dev/peps/pep-0586)
    e.g. `Literal[Literal[Literal[1, 2, 3], "foo"], 5, None]`
    """
    if not is_literal_type(type_):
        return (type_,)

    values = literal_values(type_)
    return tuple(x for value in values for x in all_literal_values(value))
