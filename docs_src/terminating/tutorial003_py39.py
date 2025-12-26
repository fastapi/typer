import typer

app = typer.Typer()


@app.command()
def main(username: str):
    if username == "root":
        print("The root user is reserved")
        raise typer.Abort()
    print(f"New user created: {username}")


if __name__ == "__main__":
    app()
