import typer
import typer.main

app = typer.Typer()


@app.command()
def main(name: str = "morty"):
    # The line below will cause TypeError because you cannot concatenate string and integer.
    print(name + 3)


if __name__ == "__main__":
    app()
