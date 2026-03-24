import typer

app = typer.Typer()


@app.command()
def main(user: list[str] | None = typer.Option(None)):
    if not user:
        print(f"No provided users (raw input = {user})")
        raise typer.Abort()
    for u in user:
        print(f"Processing user: {u}")


if __name__ == "__main__":
    app()
