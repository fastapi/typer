import typer

app = typer.Typer()


@app.command()
def main(name: str, email: str = typer.Option(..., prompt=True)):
    typer.echo(f"Hello {name}, your email is: {email}")


if __name__ == "__main__":
    app()
