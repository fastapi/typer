import typer

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def create(username: str):
    """
    [green]Create[/green] a new user. :sparkles:
    """
    print(f"Creating user: {username}")


@app.command()
def delete(username: str):
    """
    [red]Delete[/red] a user. :x:
    """
    print(f"Deleting user: {username}")


@app.command(rich_help_panel="Utils and Configs")
def config(configuration: str):
    """
    [blue]Configure[/blue] the system. :gear:
    """
    print(f"Configuring the system with: {configuration}")


@app.command(rich_help_panel="Utils and Configs")
def sync():
    """
    [blue]Synchronize[/blue] the system or something fancy like that. :recycle:
    """
    print("Syncing the system")


@app.command(rich_help_panel="Help and Others")
def help():
    """
    Get [yellow]help[/yellow] with the system. :question:
    """
    print("Opening help portal...")


@app.command(rich_help_panel="Help and Others")
def report():
    """
    [yellow]Report[/yellow] an issue. :exclamation:
    """
    print("Please open a new issue online, not a direct message")


if __name__ == "__main__":
    app()
