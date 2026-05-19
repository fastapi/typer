import typer

app = typer.Typer()


@app.command()
def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    app()
