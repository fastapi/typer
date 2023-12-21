import typer
from pydantic import EmailStr


def main(email_opt: EmailStr = typer.Option("tiangolo@gmail.com")):
    typer.echo(f"email_opt: {email_opt}")


if __name__ == "__main__":
    typer.run(main)
