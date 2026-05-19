import typer

app = typer.Typer()

users_app = typer.Typer()
app.add_typer(users_app, name="users")


@users_app.callback()
def users_callback():
    print("Running a users command")


@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
