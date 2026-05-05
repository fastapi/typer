import click
import typer
from click.shell_completion import CompletionItem

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_user_or_greeter(
    ctx: typer.Context, param: click.Parameter, incomplete: str
):
    previous_items = (ctx.params.get(param.name) if param.name else []) or []
    for item, help_text in valid_completion_items:
        if item.startswith(incomplete) and item not in previous_items:
            yield CompletionItem(item, help=help_text)


app = typer.Typer()


@app.command()
def main(
    user: list[str] = typer.Option(
        ["World"],
        help="The user to say hi to.",
        autocompletion=complete_user_or_greeter,
    ),
    greeter: list[str] = typer.Option(
        None, help="The greeters.", autocompletion=complete_user_or_greeter
    ),
):
    for u in user:
        print(f"Hello {u}, from {' and '.join(greeter or [])}")


if __name__ == "__main__":
    app()
