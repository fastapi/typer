import typer

app = typer.Typer()


@app.command()
def visible():
    """Visible command."""


@app.command(hidden=True)
def hidden_decorated():
    """Hidden via @app.command(hidden=True)."""


def hidden_var():
    """Hidden via app.command(name, hidden=True)(fn)."""


app.command("hidden-var", hidden=True)(hidden_var)

hidden_subgroup = typer.Typer(hidden=True)


@hidden_subgroup.command()
def sub():
    """Hidden subgroup command."""


app.add_typer(hidden_subgroup, name="hidden-subgroup")
