from typing import Tuple

import typer
from pydantic import AnyHttpUrl, EmailStr
from typing_extensions import Annotated


def main(
    user: Annotated[
        Tuple[str, int, EmailStr, AnyHttpUrl],
        typer.Option(help="User name, age, email and social media URL"),
    ],
):
    name, age, email, url = user
    typer.echo(f"name: {name}")
    typer.echo(f"age: {age}")
    typer.echo(f"email: {email}")
    typer.echo(f"url: {url}")


if __name__ == "__main__":
    typer.run(main)
