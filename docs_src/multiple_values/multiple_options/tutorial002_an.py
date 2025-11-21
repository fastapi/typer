from typing import List

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(number: Annotated[List[float], typer.Option()] = []):
    print(f"The sum is {sum(number)}")


if __name__ == "__main__":
    app()
