import enum

import typer
from typing_extensions import Annotated


class Access(enum.IntEnum):
    private = 1
    protected = 2
    public = 3
    open = 4


def main(access: Annotated[Access, typer.Option(enum_by_name=True)] = "private"):
    typer.echo(f"Access level: {access.name} ({access.value})")


if __name__ == "__main__":
    typer.run(main)
