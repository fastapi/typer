import typer


def main(name: str = typer.Argument("World", help="Who to greet", show_default=False)):
    """
    Say hi to NAME very gently, like Dirk.
    """
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
