import sys
from collections.abc import Callable, Sequence
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, get_args, get_origin

from pydantic import AfterValidator, BeforeValidator, Field, TypeAdapter

from ._click import _compat
from ._typing import is_literal_type, is_number_type, literal_values
from .models import ParameterInfo
from .param_types import TyperPath, _needs_typer_path, lenient_issubclass


def build_adapter(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any]:
    """Build a Pydantic TypeAdapter for a parameter annotation and metadata."""
    if parameter_info.parser is not None:
        return _build_parser_adapter(parameter_info.parser)

    origin = get_origin(annotation)
    if origin is list:
        (item_type,) = get_args(annotation)
        item_adapter = build_adapter(item_type, parameter_info)

        def parse_list(value: Any) -> list[Any]:
            if not isinstance(value, (list, tuple)):
                value = (value,)
            return [
                None if item is None else item_adapter.validate_python(item)
                for item in value
            ]

        return TypeAdapter(Annotated[list[Any], BeforeValidator(parse_list)])

    if origin is tuple:
        item_types = get_args(annotation)
        item_adapters = [
            build_adapter(item_type, parameter_info) for item_type in item_types
        ]

        def parse_tuple(value: Any) -> tuple[Any, ...]:
            if not isinstance(value, (list, tuple)):
                raise ValueError("value is not a valid tuple")
            if len(value) != len(item_adapters):
                raise ValueError(
                    f"{len(item_adapters)} values are required, but {len(value)} given."
                )
            return tuple(
                None if item is None else adapter.validate_python(item)
                for adapter, item in zip(item_adapters, value, strict=False)
            )

        return TypeAdapter(Annotated[tuple[Any, ...], BeforeValidator(parse_tuple)])

    if is_number_type(annotation):
        return build_leaf_adapter(
            annotation,
            min=parameter_info.min,
            max=parameter_info.max,
            clamp=parameter_info.clamp,
        )
    if annotation is datetime:
        return build_leaf_adapter(annotation, formats=parameter_info.formats)

    if lenient_issubclass(annotation, Enum):
        return _build_choice_adapter(
            list(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if is_literal_type(annotation):
        return _build_choice_adapter(
            literal_values(annotation),
            case_sensitive=parameter_info.case_sensitive,
        )
    if _needs_typer_path(annotation, parameter_info):
        return _build_path_adapter(annotation, parameter_info)
    return build_leaf_adapter(annotation)


def build_leaf_adapter(
    annotation: Any,
    *,
    min: float | None = None,
    max: float | None = None,
    clamp: bool = False,
    formats: Sequence[str] | None = None,
) -> TypeAdapter[Any]:
    """Build a Pydantic TypeAdapter for a leaf CLI annotation and constraints."""
    if annotation is datetime and formats is not None:
        return _build_datetime_adapter(formats)

    if is_number_type(annotation):
        if clamp:
            # Use AfterValidator so it runs after coercion
            return TypeAdapter(
                Annotated[
                    annotation,
                    AfterValidator(_make_number_clamp_validator(annotation, min, max)),
                ]
            )
        else:
            field_kwargs: dict[str, Any] = {}
            if min is not None:
                field_kwargs["ge"] = min
            if max is not None:
                field_kwargs["le"] = max
            if field_kwargs:
                return TypeAdapter(Annotated[annotation, Field(**field_kwargs)])

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
    return str(_decode_cli_bytes(value))


def _decode_cli_bytes(value: Any) -> Any:
    """Decode bytes from argv/env; leave other values unchanged."""
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
    return value


# BOOL #
def _parse_cli_bool(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            return False
        return stripped
    return value


# NUMBER #
def _make_number_clamp_validator(
    number_class: type[Any],
    min: float | None,
    max: float | None,
) -> Callable[[Any], Any]:
    def clamp_number(value: Any) -> Any:
        if min is not None and value < min:
            return number_class(min)
        if max is not None and value > max:
            return number_class(max)
        return value

    return clamp_number


# PARSER #
def _build_parser_adapter(parser: Callable[[Any], Any]) -> TypeAdapter[Any]:
    def parse_with_parser(value: Any) -> Any:
        try:
            return parser(value)
        except ValueError:
            try:
                value = str(value)
            except UnicodeError:  # pragma: no cover
                assert isinstance(value, bytes)
                value = value.decode("utf-8", "replace")
            raise ValueError(value) from None

    return TypeAdapter(Annotated[Any, BeforeValidator(parse_with_parser)])


# CHOICE #
def _normalize_choice_value(
    choice_or_value: Any,
    *,
    case_sensitive: bool,
    ctx: Any | None,
) -> str:
    if isinstance(choice_or_value, Enum):
        normed = str(choice_or_value.value)
    else:
        normed = str(choice_or_value)
    if ctx is not None and ctx.token_normalize_func is not None:
        normed = ctx.token_normalize_func(normed)
    if not case_sensitive:
        normed = normed.casefold()
    return normed


def _build_choice_adapter(
    choices: Sequence[Any],
    *,
    case_sensitive: bool,
) -> TypeAdapter[Any]:
    def normalize(choice: Any) -> str:
        return _normalize_choice_value(choice, case_sensitive=case_sensitive, ctx=None)

    mapping = {normalize(choice): choice for choice in choices}

    def parse_choice(value: Any) -> Any:
        if any(isinstance(choice, Enum) and value is choice for choice in choices):
            return value
        key = normalize(value)
        if key in mapping:
            return mapping[key]
        choices_str = ", ".join(map(repr, mapping.values()))
        raise ValueError(f"{value!r} is not one of {choices_str}.")

    return TypeAdapter(Annotated[Any, BeforeValidator(parse_choice)])


# PATH #
def _build_path_adapter(
    annotation: Any,
    parameter_info: ParameterInfo,
) -> TypeAdapter[Any]:
    path_type = parameter_info.path_type
    if path_type is None and lenient_issubclass(annotation, Path):
        path_type = annotation

    typer_path = TyperPath(
        exists=parameter_info.exists,
        file_okay=parameter_info.file_okay,
        dir_okay=parameter_info.dir_okay,
        writable=parameter_info.writable,
        readable=parameter_info.readable,
        resolve_path=parameter_info.resolve_path,
        allow_dash=parameter_info.allow_dash,
        path_type=path_type,
    )

    def parse_path(value: Any) -> Any:
        return typer_path.convert(value, param=None, ctx=None)

    return TypeAdapter(Annotated[Any, BeforeValidator(parse_path)])
