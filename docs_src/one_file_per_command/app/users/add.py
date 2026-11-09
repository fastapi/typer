import typer

app = typer.Typer()


@app.command()
def add(name: str):
    print(f"Adding user: {name}")
