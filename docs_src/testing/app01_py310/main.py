import typer

app = typer.Typer()


@app.command()
def main(name: str, city: str | None = None):
    print(f"Hello {name}")
    if city:
        print(f"Let's have a coffee in {city}")


if __name__ == "__main__":
    app()
