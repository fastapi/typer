import typer


def complete_name():
    return ["Camila", "Carlos", "Sebastian"]


def main(
    name: str = typer.Option(
        "World", help="The name to say hi to.", autocompletion=complete_name
    )
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
