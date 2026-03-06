from typing import Annotated

import typer
from pydantic import AnyHttpUrl, IPvAnyAddress

app = typer.Typer()


@app.command()
def main(
    server: Annotated[
        tuple[str, IPvAnyAddress, AnyHttpUrl],
        typer.Option(help="User name, age, email and social media URL"),
    ],
):
    name, address, url = server
    typer.echo(f"name: {name}")
    typer.echo(f"address: {address}")
    typer.echo(f"url: {url}")


if __name__ == "__main__":
    app()
