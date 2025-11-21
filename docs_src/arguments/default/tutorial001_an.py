import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(name: Annotated[str, typer.Argument()] = "Wade Wilson"):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
