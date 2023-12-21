import typer
from pydantic import EmailStr


def main(email_arg: EmailStr):
    typer.echo(f"email_arg: {email_arg}")


if __name__ == "__main__":
    typer.run(main)
