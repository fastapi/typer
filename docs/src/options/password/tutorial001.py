import typer


def main(
    name: str, email: str = typer.Option(..., prompt=True, confirmation_prompt=True)
):
    typer.echo(f"Hello {name}, your email is {email}")


if __name__ == "__main__":
    typer.run(main)
