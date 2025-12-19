from typing import List

import typer

app = typer.Typer()


@app.command()
def main(number: List[float] = typer.Option([], separator=",")):
    print(f"The sum is {sum(number)}")


if __name__ == "__main__":
    app()
