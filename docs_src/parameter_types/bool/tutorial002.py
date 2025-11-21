from typing import Optional

import typer

app = typer.Typer()


@app.command()
def main(accept: Optional[bool] = typer.Option(None, "--accept/--reject")):
    if accept is None:
        print("I don't know what you want yet")
    elif accept:
        print("Accepting!")
    else:
        print("Rejecting!")


if __name__ == "__main__":
    app()
