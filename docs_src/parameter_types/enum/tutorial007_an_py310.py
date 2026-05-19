import enum
import logging
from typing import Annotated

import typer


class LogLevel(enum.Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING


app = typer.Typer()


@app.command()
def main(log_level: Annotated[LogLevel, typer.Option(enum_by_name=True)] = "warning"):
    typer.echo(f"Log level set to: {logging.getLevelName(log_level.value)}")


if __name__ == "__main__":
    app()
