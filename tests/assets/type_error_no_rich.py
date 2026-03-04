import typer
import typer.main

typer.main.HAS_RICH = False

app = typer.Typer()


@app.command()
def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    app()
