from typing import Annotated, Optional

import typer

app = typer.Typer()


@app.command()
def main(accept: Annotated[Optional[bool], typer.Option("--accept/--reject")] = None):
    if accept is None:
        print("I don't know what you want yet")
    elif accept:
        print("Accepting!")
    else:
        print("Rejecting!")


if __name__ == "__main__":
    app()
