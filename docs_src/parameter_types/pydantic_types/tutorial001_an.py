import typer
from pydantic import AnyHttpUrl
from typing_extensions import Annotated


def main(url_arg: Annotated[AnyHttpUrl, typer.Argument()]):
    typer.echo(f"url_arg: {url_arg}")


if __name__ == "__main__":
    typer.run(main)
