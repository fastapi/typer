from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(borrow: Annotated[list[tuple[float, str]], typer.Option()] = []):
    if not borrow:
        print("Congratulations, you're debt-free!")
        raise typer.Exit(0)
    total = 0.0
    for amount, person in borrow:
        print(f"Borrowed {amount:.2f} from {person}")
        total += amount
    print()
    print(f"Total borrowed: {total:.2f}")


if __name__ == "__main__":
    app()
