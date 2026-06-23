import sys
from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, get_args, get_origin

from pydantic import AfterValidator, BeforeValidator, Field, TypeAdapter, ValidationInfo
from pydantic.errors import PydanticSchemaGenerationError

from ._click import _compat
from ._typing import is_literal_type, is_number_type, literal_values
from .models import ParameterInfo
from .param_types import (
    _needs_typer_path,
    coerce_cli_choice,
    coerce_cli_path,
    lenient_issubclass,
)

if TYPE_CHECKING:
    from ._click import Context
    from .core import TyperParameter

_CTX_KEY = "ctx"
_PARAM_KEY = "param"


def validation_context(
    ctx: "Context",
    param: "TyperParameter",
) -> dict[str, Any]:
    return {_CTX_KEY: ctx, _PARAM_KEY: param}


def validation_ctx_param(
    info: ValidationInfo,
) -> tuple["Context | None", "TyperParameter | None"]:
    context = info.context
    if not context:
        return None, None
    return context.get(_CTX_KEY), context.get(_PARAM_KEY)


def try_build_adapter(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any] | None:
    """Build a TypeAdapter when Pydantic can schema-generate the annotation."""
    try:
        return build_adapter(annotation, parameter_info)
    except PydanticSchemaGenerationError:
        return None


def build_adapter(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any]:
    """Build a Pydantic TypeAdapter for a parameter annotation and metadata.
    Check for list/tuple and call this function recursively.
    Otherwise, delegate to build_leaf_adapter.
    """
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if len(args) != 1:
            raise ValueError(f"Expected one list item type, got: {args!r}")
        list_type = args[0]
        adapter = build_adapter(list_type, parameter_info)

        def parse_list(value: Any, info: ValidationInfo) -> list[Any]:
            if not isinstance(value, (list, tuple)):
                value = [value]
            context = info.context
            return [
                None if item is None else adapter.validate_python(item, context=context)
                for item in value
            ]

        return TypeAdapter(Annotated[list[Any], BeforeValidator(parse_list)])

    if origin is tuple:
        types = get_args(annotation)
        adapters = [build_adapter(t, parameter_info) for t in types]

        def parse_tuple(value: Any, info: ValidationInfo) -> tuple[Any, ...]:
            if not isinstance(value, (list, tuple)):
                raise ValueError("value is not a valid tuple")
            if len(value) != len(adapters):
                raise ValueError(
                    f"{len(adapters)} values are required, but {len(value)} given."
                )
            context = info.context
            return tuple(
                None if item is None else adapter.validate_python(item, context=context)
                for adapter, item in zip(adapters, value, strict=False)
            )

        return TypeAdapter(Annotated[tuple[Any, ...], BeforeValidator(parse_tuple)])

    return build_leaf_adapter(annotation, parameter_info=parameter_info)


def build_leaf_adapter(
    annotation: Any,
    *,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any]:
    """Build a Pydantic TypeAdapter for a leaf CLI annotation and constraints."""
    if parameter_info.parser is not None:
        parser = parameter_info.parser

        # We need this because Pydantic would otherwise reject a callable class
        def parse(value: Any) -> Any:
            return parser(value)

        return TypeAdapter(Annotated[Any, BeforeValidator(parse)])

    if lenient_issubclass(annotation, Enum):
        case_sensitive = parameter_info.case_sensitive
        return _build_choice_adapter(
            list(annotation),
            case_sensitive=case_sensitive,
        )
    if is_literal_type(annotation):
        case_sensitive = parameter_info.case_sensitive
        return _build_choice_adapter(
            literal_values(annotation),
            case_sensitive=case_sensitive,
        )
    if _needs_typer_path(annotation, parameter_info):
        return build_path_adapter(annotation, parameter_info)

    if annotation is datetime:
        return _build_datetime_adapter(parameter_info.formats)

    if is_number_type(annotation):
        return _build_number_adapter(
            annotation,
            min=parameter_info.min,
            max=parameter_info.max,
            clamp=parameter_info.clamp,
        )

    if annotation is bool:
        return TypeAdapter(Annotated[bool, BeforeValidator(_parse_cli_bool)])

    if annotation is str:
        return TypeAdapter(Annotated[str, BeforeValidator(_parse_cli_str)])

    return TypeAdapter(annotation)


# DATE #
def _build_datetime_adapter(formats: Sequence[str] | None) -> TypeAdapter[datetime]:
    if formats is None:
        return TypeAdapter(datetime)

    def parse_datetime(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        for format in formats:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                continue
        formats_str = ", ".join(map(repr, formats))
        raise ValueError(f"{value!r} does not match the formats {formats_str}.")

    return TypeAdapter(Annotated[datetime, BeforeValidator(parse_datetime)])


# STRING / BYTES #
def _parse_cli_str(value: Any) -> str:
    """Coerce a CLI value to str"""
    if isinstance(value, bytes):
        enc = _compat._get_argv_encoding()
        try:
            return value.decode(enc)
        except UnicodeError:
            fs_enc = sys.getfilesystemencoding()
            if fs_enc != enc:
                try:
                    return value.decode(fs_enc)
                except UnicodeError:
                    return value.decode("utf-8", "replace")
            return value.decode("utf-8", "replace")
    return str(value)


# BOOL #
def _parse_cli_bool(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    stripped = value.strip()
    if stripped == "":
        return False
    return stripped


# NUMBER #
def _build_number_adapter(
    number_class: type[Any], *, min: float | None, max: float | None, clamp: bool | None
) -> TypeAdapter[Any]:
    if clamp:

        def clamp_number(value: Any) -> Any:
            if min is not None and value < min:
                return number_class(min)
            if max is not None and value > max:
                return number_class(max)
            return value

        # Use AfterValidator so it runs after coercion
        return TypeAdapter(Annotated[number_class, AfterValidator(clamp_number)])  # ty: ignore[invalid-type-form]
    else:
        field_kwargs: dict[str, Any] = {}
        if min is not None:
            field_kwargs["ge"] = min
        if max is not None:
            field_kwargs["le"] = max
        if field_kwargs:
            return TypeAdapter(Annotated[number_class, Field(**field_kwargs)])  # ty: ignore[invalid-type-form]
        return TypeAdapter(number_class)


# CHOICE #
def _build_choice_adapter(
    choices: Sequence[Any],
    *,
    case_sensitive: bool,
) -> TypeAdapter[Any]:
    def parse_choice(value: Any, info: ValidationInfo) -> Any:
        ctx, _ = validation_ctx_param(info)
        return coerce_cli_choice(
            value,
            choices=choices,
            case_sensitive=case_sensitive,
            ctx=ctx,
        )

    return TypeAdapter(Annotated[Any, BeforeValidator(parse_choice)])


# PATH #
def build_path_adapter(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any]:
    path_type = parameter_info.path_type
    if path_type is None and lenient_issubclass(annotation, Path):
        path_type = annotation

    def parse_path(value: Any, info: ValidationInfo) -> Any:
        ctx, param = validation_ctx_param(info)
        return coerce_cli_path(
            value,
            parameter_info,
            path_type=path_type,
            param=param,
            ctx=ctx,
        )

    return TypeAdapter(Annotated[Any, BeforeValidator(parse_path)])
