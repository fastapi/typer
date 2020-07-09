import typer


def main(username: str):
    if username == "root":
        typer.echo("The root user is reserved")
        raise typer.Abort()
    typer.echo(f"New user created: {username}")


if __name__ == "__main__":
    typer.run(main)
