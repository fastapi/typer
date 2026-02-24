from typing import Annotated

import typer


def complete_user():
    return ["Camila", "Carlos", "Sebastian"]


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        str, typer.Option(help="The user to say hi to.", autocompletion=complete_user)
    ] = "World",
):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
