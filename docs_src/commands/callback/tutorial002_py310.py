import typer


def callback():
    print("Running a command")


app = typer.Typer(callback=callback)


@app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
