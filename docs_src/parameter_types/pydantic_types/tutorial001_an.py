import typer
from pydantic import EmailStr
from typing_extensions import Annotated


def main(email_arg: Annotated[EmailStr, typer.Argument()]):
    typer.echo(f"email_arg: {email_arg}")


if __name__ == "__main__":
    typer.run(main)
