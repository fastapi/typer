from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(name: Annotated[str, typer.Argument(hidden=True)] = "World"):
    """
    Say hi to NAME very gently, like Dirk.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
