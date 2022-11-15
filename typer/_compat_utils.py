import click


def _get_click_major() -> int:
    return int(click.__version__.split(".", maxsplit=1)[0])
