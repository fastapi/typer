import typer
from rich.console import Console
from rich.table import Table

console = Console()


def main():
    table = Table("Name", "Item")
    table.add_row("Rick", "Portal Gun")
    table.add_row("Morty", "Plumbus")
    console.print(table)


if __name__ == "__main__":
    typer.run(main)
