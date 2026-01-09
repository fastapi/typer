from typing import List

import typer

app = typer.Typer()


@app.command()
def main(user: List[str] = typer.Option(["World"], help="The user to say hi to.")):
    for u in user:
        print(f"Hello {u}")


if __name__ == "__main__":
    app()
