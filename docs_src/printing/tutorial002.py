import typer
from rich import print

app = typer.Typer()


@app.command()
def main():
    print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")


if __name__ == "__main__":
    app()
