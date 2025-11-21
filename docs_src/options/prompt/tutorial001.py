import typer

app = typer.Typer()


@app.command()
def main(name: str, lastname: str = typer.Option(..., prompt=True)):
    print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    app()
