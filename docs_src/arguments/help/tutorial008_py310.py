import typer

app = typer.Typer()


@app.command()
def main(name: str = typer.Argument("World", hidden=True)):
    """
    Say hi to NAME very gently, like Dirk.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
