from typing import List

import typer
from pydantic import AnyHttpUrl
from typing_extensions import Annotated


def main(
    urls: Annotated[List[AnyHttpUrl], typer.Option("--url", default_factory=list)],
):
    typer.echo(f"urls: {urls}")


if __name__ == "__main__":
    typer.run(main)
