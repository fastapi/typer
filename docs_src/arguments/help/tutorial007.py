from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    name: Annotated[str, typer.Argument(help="Who to greet")],
    lastname: Annotated[
        str, typer.Argument(help="The last name", rich_help_panel="Secondary Arguments")
    ] = "",
    age: Annotated[
        str,
        typer.Argument(help="The user's age", rich_help_panel="Secondary Arguments"),
    ] = "",
):
    """
    Say hi to 'name' very gently, like Dirk.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
