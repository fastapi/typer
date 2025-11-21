import typer

app = typer.Typer()


@app.command()
def main(name: str = typer.Argument("World", metavar="✨username✨")):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
