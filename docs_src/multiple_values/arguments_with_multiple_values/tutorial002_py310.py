import typer

app = typer.Typer()


@app.command()
def main(
    names: tuple[str, str, str] = typer.Argument(
        ("Harry", "Hermione", "Ron"), help="Select 3 characters to play with"
    ),
):
    for name in names:
        print(f"Hello {name}")


if __name__ == "__main__":
    app()
