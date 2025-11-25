import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(verbose: Annotated[int, typer.Option("--verbose", "-v", count=True)] = 0):
    print(f"Verbose level is {verbose}")


if __name__ == "__main__":
    app()
