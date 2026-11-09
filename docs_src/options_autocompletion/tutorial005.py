from typing import Annotated

import typer

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(incomplete: str):
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)


app = typer.Typer()


@app.command()
def main(
    name: Annotated[
        str, typer.Option(help="The name to say hi to.", autocompletion=complete_name)
    ] = "World",
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
