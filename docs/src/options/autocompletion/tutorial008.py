from typing import List

import typer

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(args: List[str], incomplete: str):
    typer.echo(f"{args}", err=True)
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)


def main(
    name: List[str] = typer.Option(
        ["World"], help="The name to say hi to.", autocompletion=complete_name
    )
):
    for n in name:
        typer.echo(f"Hello {n}")


if __name__ == "__main__":
    typer.run(main)
