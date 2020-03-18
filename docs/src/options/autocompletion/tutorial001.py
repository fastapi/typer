import typer


def main(name: str = typer.Option("World", help="The name to say hi to.")):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
