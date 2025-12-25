# Copied from pydantic 1.9.2 (the latest version to support python 3.6.)
# https://github.com/pydantic/pydantic/blob/v1.9.2/pydantic/typing.py
# Reduced drastically to only include Typer-specific 3.9+ functionality
# mypy: ignore-errors

import sys
from typing import (
    Annotated,
    Any,
    Callable,
    Literal,
    Optional,
    Tuple,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

if sys.version_info < (3, 10):

    def is_union(tp: Optional[Type[Any]]) -> bool:
        return tp is Union

else:
    import types

    def is_union(tp: Optional[Type[Any]]) -> bool:
        return tp is Union or tp is types.UnionType  # noqa: E721


if sys.version_info < (3, 12):
    from typing_extensions import TypeAliasType, TypeVar
else:
    from typing import TypeAliasType, TypeVar

__all__ = (
    "NoneType",
    "is_none_type",
    "is_callable_type",
    "is_literal_type",
    "all_literal_values",
    "is_union",
    "Annotated",
    "Literal",
    "TypeAliasType",
    "TypeVar",
    "get_args",
    "get_origin",
    "get_type_hints",
)


NoneType = None.__class__


NONE_TYPES: Tuple[Any, Any, Any] = (None, NoneType, Literal[None])


def is_none_type(type_: Any) -> bool:
    for none_type in NONE_TYPES:
        if type_ is none_type:
            return True
    return False


def is_callable_type(type_: Type[Any]) -> bool:
    return type_ is Callable or get_origin(type_) is Callable


def is_literal_type(type_: Type[Any]) -> bool:
    import typing_extensions

    return get_origin(type_) in (Literal, typing_extensions.Literal)


def literal_values(type_: Type[Any]) -> Tuple[Any, ...]:
    return get_args(type_)


def all_literal_values(type_: Type[Any]) -> Tuple[Any, ...]:
    """
    This method is used to retrieve all Literal values as
    Literal can be used recursively (see https://www.python.org/dev/peps/pep-0586)
    e.g. `Literal[Literal[Literal[1, 2, 3], "foo"], 5, None]`
    """
    if not is_literal_type(type_):
        return (type_,)

    values = literal_values(type_)
    return tuple(x for value in values for x in all_literal_values(value))
