import typer

app = typer.Typer()


@app.command()
def found(name: str):
    print(f"Founding town: {name}")


@app.command()
def burn(name: str):
    print(f"Burning town: {name}")


if __name__ == "__main__":
    app()
