from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(name: str, lastname: Annotated[str, typer.Option()]):
    print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    app()
