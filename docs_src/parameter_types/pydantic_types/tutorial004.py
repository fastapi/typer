from typing import Tuple

import typer
from pydantic import AnyHttpUrl, IPvAnyAddress


def main(
    server: Tuple[str, IPvAnyAddress, AnyHttpUrl] = typer.Option(
        ..., help="Server name, IP address and public URL"
    ),
):
    name, address, url = server
    typer.echo(f"name: {name}")
    typer.echo(f"address: {address}")
    typer.echo(f"url: {url}")


if __name__ == "__main__":
    typer.run(main)
