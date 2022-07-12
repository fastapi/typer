import typer


def main(
    name: str,
    lastname: str = typer.Option("", help="Last name of person to greet."),
    formal: bool = typer.Option(
        False, help="Say hi formally.", rich_help_panel="Customization and Utils"
    ),
    debug: bool = typer.Option(
        False, help="Enable debugging.", rich_help_panel="Customization and Utils"
    ),
):
    """
    Say hi to NAME, optionally with a --lastname.

    If --formal is used, say hi very formally.
    """
    if formal:
        print(f"Good day Ms. {name} {lastname}.")
    else:
        print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    typer.run(main)
