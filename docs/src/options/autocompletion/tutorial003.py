import typer

valid_names = ["Camila", "Carlos", "Sebastian"]


def complete_name(incomplete: str):
    completion = []
    for name in valid_names:
        if name.startswith(incomplete):
            completion.append(name)
    return completion


def main(
    name: str = typer.Option(
        "World", help="The name to say hi to.", autocompletion=complete_name
    )
):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
