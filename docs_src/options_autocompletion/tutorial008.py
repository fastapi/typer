from typing import List

from rich.console import Console
import typer

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]

err_console = Console(stderr=True)


def complete_name(args: List[str], incomplete: str):
    err_console.print(f"{args}")
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)


app = typer.Typer()


@app.command()
def main(
    name: List[str] = typer.Option(
        ["World"], help="The name to say hi to.", autocompletion=complete_name
    )
):
    for n in name:
        print(f"Hello {n}")


if __name__ == "__main__":
    app()
