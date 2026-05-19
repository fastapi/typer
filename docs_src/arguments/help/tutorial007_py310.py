import typer

app = typer.Typer()


@app.command()
def main(
    name: str = typer.Argument(..., help="Who to greet"),
    lastname: str = typer.Argument(
        "", help="The last name", rich_help_panel="Secondary Arguments"
    ),
    age: str = typer.Argument(
        "", help="The user's age", rich_help_panel="Secondary Arguments"
    ),
):
    """
    Say hi to NAME very gently, like Dirk.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
