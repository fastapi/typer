from typing import Annotated

import typer
from pydantic import AnyHttpUrl

app = typer.Typer()


@app.command()
def main(
    urls: Annotated[list[AnyHttpUrl], typer.Option("--url", default_factory=list)],
):
    typer.echo(f"urls: {urls}")


if __name__ == "__main__":
    app()
