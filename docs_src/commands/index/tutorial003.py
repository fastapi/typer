import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


if __name__ == "__main__":
    app()
