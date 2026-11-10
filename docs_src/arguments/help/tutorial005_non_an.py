import typer

app = typer.Typer()


@app.command()
def main(
    name: str = typer.Argument(
        "Wade Wilson", help="Who to greet", show_default="Deadpoolio the amazing's name"
    ),
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
