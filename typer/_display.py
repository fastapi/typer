from typing import Any

from ._click.utils import _escape_control_characters


def describe_number_range(
    min: int | float | None,
    max: int | float | None,
) -> str | None:
    if min is None and max is None:
        return None
    if min is None:
        return f"x<={max}"
    if max is None:
        return f"x>={min}"
    return f"{min}<=x<={max}"


def get_error_msg(exc: Any) -> str:
    """Get the first validation error message with terminal controls escaped."""
    errors = exc.errors()
    if errors:
        return _escape_control_characters(str(errors[0]["msg"]))
    return _escape_control_characters(str(exc))  # pragma: no cover
