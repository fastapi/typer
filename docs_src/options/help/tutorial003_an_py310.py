from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(fullname: Annotated[str, typer.Option(show_default=False)] = "Wade Wilson"):
    print(f"Hello {fullname}")


if __name__ == "__main__":
    app()
