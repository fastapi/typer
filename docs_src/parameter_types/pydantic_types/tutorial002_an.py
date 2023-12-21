import typer
from pydantic import EmailStr
from typing_extensions import Annotated


def main(email_opt: Annotated[EmailStr, typer.Option()] = "tiangolo@gmail.com"):
    typer.echo(f"email_opt: {email_opt}")


if __name__ == "__main__":
    typer.run(main)
