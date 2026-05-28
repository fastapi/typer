from typing import Annotated

import typer

app = typer.Typer(rich_markup_mode="markdown")


@app.command()
def create(
    username: Annotated[str, typer.Argument(help="The username to be **created**")],
):
    """
    **Create** a new *shiny* user. :sparkles:

    * Create a username

    * Show that the username is created

    ---

    Learn more at the [Typer docs website](https://typer.tiangolo.com)
    """
    print(f"Creating user: {username}")


@app.command(help="**Delete** a user with *USERNAME*.")
def delete(
    username: Annotated[str, typer.Argument(help="The username to be **deleted**")],
    force: Annotated[bool, typer.Option(help="Force the **deletion** :boom:")] = False,
):
    """
    Some internal utility function to delete.
    """
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
