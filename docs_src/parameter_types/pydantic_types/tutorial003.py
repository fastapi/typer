from typing import List

import typer
from pydantic import AnyHttpUrl


def main(urls: List[AnyHttpUrl] = typer.Option([], "--url")):
    typer.echo(f"urls: {urls}")


if __name__ == "__main__":
    typer.run(main)
