from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(user_name: Annotated[str, typer.Option("--user-name", "-n")]):
    print(f"Hello {user_name}")


if __name__ == "__main__":
    app()
