import typer

app = typer.Typer()


@app.command()
def main(name: str = typer.Option("World", help="The name to say hi to.")):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
