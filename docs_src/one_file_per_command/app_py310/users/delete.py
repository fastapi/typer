import typer

app = typer.Typer()


@app.command()
def delete(name: str):
    print(f"Deleting user: {name}")
