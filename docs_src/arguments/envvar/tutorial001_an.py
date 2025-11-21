import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(name: Annotated[str, typer.Argument(envvar="AWESOME_NAME")] = "World"):
    print(f"Hello Mr. {name}")


if __name__ == "__main__":
    app()
