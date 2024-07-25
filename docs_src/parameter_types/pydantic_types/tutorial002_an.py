import typer
from pydantic import AnyHttpUrl
from typing_extensions import Annotated


def main(url_opt: Annotated[AnyHttpUrl, typer.Option()] = "tiangolo@gmail.com"):
    typer.echo(f"url_opt: {url_opt}")


if __name__ == "__main__":
    typer.run(main)
