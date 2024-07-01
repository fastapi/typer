import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def main(name: str, email: Annotated[str, typer.Option(prompt=True)]):
    print(f"Hello {name}, your email is: {email}")


if __name__ == "__main__":
    app()
