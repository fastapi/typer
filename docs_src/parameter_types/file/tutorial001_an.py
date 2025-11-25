import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(config: Annotated[typer.FileText, typer.Option()]):
    for line in config:
        print(f"Config line: {line}")


if __name__ == "__main__":
    app()
