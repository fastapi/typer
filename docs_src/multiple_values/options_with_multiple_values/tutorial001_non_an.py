import typer

app = typer.Typer()


@app.command()
def main(user: tuple[str, int, bool] | None = typer.Option(None)):
    if not user:
        print("No user provided")
        raise typer.Abort()
    username, coins, is_wizard = user
    print(f"The username {username} has {coins} coins")
    if is_wizard:
        print("And this user is a wizard!")


if __name__ == "__main__":
    app()
