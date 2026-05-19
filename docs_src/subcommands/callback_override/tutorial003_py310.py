import typer

app = typer.Typer()


def default_callback():
    print("Running a users command")


users_app = typer.Typer(callback=default_callback)
app.add_typer(users_app, name="users")


@users_app.callback()
def user_callback():
    print("Callback override, running users command")


@users_app.command()
def create(name: str):
    print(f"Creating user: {name}")


if __name__ == "__main__":
    app()
