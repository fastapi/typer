import enum
import logging

import typer
from typing_extensions import Annotated


class LogLevel(enum.Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING


def main(log_level: Annotated[LogLevel, typer.Option(enum_by_name=True)] = "warning"):
    typer.echo(f"Log level set to: {logging.getLevelName(log_level.value)}")


if __name__ == "__main__":
    typer.run(main)
