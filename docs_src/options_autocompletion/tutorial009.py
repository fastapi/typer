from typing import List

import typer
from click.core import Parameter
from rich.console import Console

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]

err_console = Console(stderr=True)


def complete_name(ctx: typer.Context, param: Parameter, incomplete: str):
    names = ctx.params.get(param.name) or []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete) and name not in names:
            yield (name, help_text)


app = typer.Typer()


@app.command()
def main(
    name: List[str] = typer.Option(
        ["World"], help="The name to say hi to.", autocompletion=complete_name
    ),
):
    for n in name:
        print(f"Hello {n}")


if __name__ == "__main__":
    app()
