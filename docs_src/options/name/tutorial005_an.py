import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(
    name: Annotated[str, typer.Option("--name", "-n")],
    formal: Annotated[bool, typer.Option("--formal", "-f")] = False,
):
    if formal:
        print(f"Good day Ms. {name}.")
    else:
        print(f"Hello {name}")


if __name__ == "__main__":
    app()
