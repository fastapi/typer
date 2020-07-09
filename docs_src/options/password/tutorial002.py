import typer


def main(
    name: str,
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True
    ),
):
    typer.echo(f"Hello {name}. Doing something very secure with password.")
    typer.echo(f"...just kidding, here it is, very insecure: {password}")


if __name__ == "__main__":
    typer.run(main)
