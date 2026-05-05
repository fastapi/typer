from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(
    user: Annotated[list[str], typer.Option(help="The user to say hi to.")] = ["World"],
):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
