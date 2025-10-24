import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(user: Annotated[str, typer.Option(help="The user to say hi to.")] = "World"):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
