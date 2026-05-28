from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(name: Annotated[str, typer.Option(help="The name to say hi to.")] = "World"):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
