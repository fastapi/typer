import typer

app = typer.Typer()


@app.command()
def conquer(name: str):
    print(f"Conquering reign: {name}")


@app.command()
def destroy(name: str):
    print(f"Destroying reign: {name}")


if __name__ == "__main__":
    app()
