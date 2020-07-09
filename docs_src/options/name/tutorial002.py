import typer


def main(user_name: str = typer.Option(..., "--name", "-n")):
    typer.echo(f"Hello {user_name}")


if __name__ == "__main__":
    typer.run(main)
