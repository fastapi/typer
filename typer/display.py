from pydantic import ValidationError


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


def get_error_msg(exc: ValidationError) -> str:
    """Get a string representation of the (first) validation error."""
    errors = exc.errors()
    if errors:
        return errors[0]["msg"]
    return str(exc)
