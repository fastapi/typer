import enum
import logging

import typer


class LogLevel(enum.Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING


def main(log_level: LogLevel = typer.Option("warning", enum_by_name=True)):
    typer.echo(f"Log level set to: {logging.getLevelName(log_level.value)}")


if __name__ == "__main__":
    typer.run(main)
