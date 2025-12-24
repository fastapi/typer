from typing import Annotated, List

import typer

app = typer.Typer()


@app.command()
def main(
    name: Annotated[List[str], typer.Option(help="The name to say hi to.")] = ["World"],
):
    for each_name in name:
        print(f"Hello {each_name}")


if __name__ == "__main__":
    app()
