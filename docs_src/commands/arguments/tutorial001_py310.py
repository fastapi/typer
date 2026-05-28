import typer

app = typer.Typer()


@app.command()
def create(username: str):
    print(f"Creating user: {username}")


@app.command()
def delete(username: str):
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
