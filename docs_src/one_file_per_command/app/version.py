import typer

app = typer.Typer()


@app.command()
def version():
    print("My CLI Version 1.0")
