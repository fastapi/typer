import sys
from collections.abc import Callable, Sequence
from datetime import datetime
from typing import Annotated, Any

from pydantic import AfterValidator, BeforeValidator, Field, TypeAdapter


def _build_datetime_adapter(
    formats: Sequence[str] | None,
) -> TypeAdapter[datetime]:
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


_bool_adapter = TypeAdapter(bool)


def decode_cli_bytes(value: Any) -> Any:
    """Decode bytes from argv/env; leave other values unchanged."""
    if isinstance(value, bytes):
        from ._click import _compat

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


def _parse_cli_str(value: Any) -> str:
    """Coerce a CLI value to str"""
    return str(decode_cli_bytes(value))


def _parse_cli_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            return False
        value = stripped
    return _bool_adapter.validate_python(value)


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


def build_type_adapter(
    annotation: Any,
    *,
    min: float | None = None,
    max: float | None = None,
    clamp: bool = False,
    formats: Sequence[str] | None = None,
) -> TypeAdapter[Any]:
    """Build a Pydantic TypeAdapter for a CLI annotation and constraints.

    Known constraints (ranges, custom datetime formats, etc.) are applied first,
    everything else is delegated to Pydantic.
    """
    if annotation is datetime and formats is not None:
        return _build_datetime_adapter(formats)

    if annotation is int or annotation is float:
        if clamp:
            # Use AfterValidator so it runs after coercion
            return TypeAdapter(
                Annotated[
                    annotation,
                    AfterValidator(_make_number_clamp_validator(annotation, min, max)),
                ]
            )
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
