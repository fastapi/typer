from typing import Tuple

import typer
from pydantic import AnyHttpUrl, IPvAnyAddress
from typing_extensions import Annotated


def main(
    server: Annotated[
        Tuple[str, IPvAnyAddress, AnyHttpUrl],
        typer.Option(help="User name, age, email and social media URL"),
    ],
):
    name, address, url = server
    typer.echo(f"name: {name}")
    typer.echo(f"address: {address}")
    typer.echo(f"url: {url}")


if __name__ == "__main__":
    typer.run(main)
