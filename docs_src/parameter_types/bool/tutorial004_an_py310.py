from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(in_prod: Annotated[bool, typer.Option(" /--demo", " /-d")] = True):
    if in_prod:
        print("Running in production")
    else:
        print("Running demo")


if __name__ == "__main__":
    app()
