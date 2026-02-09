from typer import _click


@_click.command()
@_click.option("--count", default=1, help="Number of greetings.")
@_click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        _click.echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()
