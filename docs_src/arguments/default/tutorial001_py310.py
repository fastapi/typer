import typer

app = typer.Typer()


@app.command()
def main(name: str = typer.Argument("Wade Wilson")):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
