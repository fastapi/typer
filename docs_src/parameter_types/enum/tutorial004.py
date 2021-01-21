import enum

import typer


class Access(enum.IntEnum):
    private = 1
    protected = 2
    public = 3
    open = 4


def main(access: Access = typer.Option(Access.private)):
    typer.echo(f"Access level: {access.name}")


if __name__ == "__main__":
    typer.run(main)
