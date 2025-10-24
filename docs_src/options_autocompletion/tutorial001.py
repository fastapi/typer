import typer

app = typer.Typer()


@app.command()
def main(user: str = typer.Option("World", help="The user to say hi to.")):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
