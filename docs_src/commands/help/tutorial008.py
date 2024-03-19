import typer

app = typer.Typer(rich_markup_mode="rich")


@app.command(epilog="Made with :heart: in [blue]Venus[/blue]")
def create(username: str):
    """
    [green]Create[/green] a new user. :sparkles:
    """
    print(f"Creating user: {username}")


if __name__ == "__main__":
    app()
