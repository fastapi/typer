import click
import typer

app = typer.Typer()


@app.command()
def top():
    """
    Top level command, form Typer
    """
    print("The Typer app is at the top level")


@app.callback()
def callback():
    """
    Typer app, including Click subapp
    """


@click.command()
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(name):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"Hello {name}!")


typer_click_object = typer.main.get_command(app)

typer_click_object.add_command(hello, "hello")

if __name__ == "__main__":
    typer_click_object()
