import typer
import typer.main

typer.main.HAS_RICH = False


app = typer.Typer(pretty_exceptions_short=False)


@app.command()
def main(name: str = "morty"):
    print(name + 3)


if __name__ == "__main__":
    app()
