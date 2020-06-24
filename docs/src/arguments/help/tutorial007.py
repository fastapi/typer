import typer


def main(name: str = typer.Argument("World", hidden=True)):
    """
    Say hi to NAME very gently, like Dirk.
    """
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
