import typer

app = typer.Typer()


@app.command()
def main(name: str, city: str = None):
    typer.echo(f"Hello {name}")
    if city:
        typer.echo(f"Let's have a coffee in {city}")


if __name__ == "__main__":
    app()
