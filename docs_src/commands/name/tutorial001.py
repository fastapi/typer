import typer

app = typer.Typer()


@app.command("create")
def cli_create_user(username: str):
    print(f"Creating user: {username}")


@app.command("delete")
def cli_delete_user(username: str):
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
