from typing import List

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(
    user: Annotated[List[str], typer.Option(help="The user to say hi to.")] = ["World"],
):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
