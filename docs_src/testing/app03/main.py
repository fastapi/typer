import typer


def main(name: str = "World"):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
