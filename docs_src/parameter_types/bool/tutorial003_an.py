import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(force: Annotated[bool, typer.Option("--force/--no-force", "-f/-F")] = False):
    if force:
        print("Forcing operation")
    else:
        print("Not forcing")


if __name__ == "__main__":
    app()
