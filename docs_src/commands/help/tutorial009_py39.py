from typing import Union

import typer

app = typer.Typer(rich_markup_mode="rich", rich_expand=False)


@app.command()
def create(
    username: str = typer.Argument(..., help="The username"),
    lastname: str = typer.Argument(
        "", help="The last name", rich_help_panel="Secondary Arguments"
    ),
    force: bool = typer.Option(..., help="Force the creation"),
    age: Union[int, None] = typer.Option(
        None, help="The age", rich_help_panel="Additional Data"
    ),
    favorite_color: Union[str, None] = typer.Option(
        None,
        help="The favorite color",
        rich_help_panel="Additional Data",
    ),
):
    """
    [green]Create[/green] a new user. :sparkles:
    """
    print(f"Creating user: {username}")


@app.command(rich_help_panel="Utils and Configs")
def config(configuration: str):
    """
    [blue]Configure[/blue] the system. :gear:
    """
    print(f"Configuring the system with: {configuration}")


if __name__ == "__main__":
    app()
