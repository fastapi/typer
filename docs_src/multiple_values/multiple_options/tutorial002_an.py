from typing import Annotated, List

import typer

app = typer.Typer()


@app.command()
def main(number: Annotated[List[float], typer.Option()] = []):
    print(f"The sum is {sum(number)}")


if __name__ == "__main__":
    app()
