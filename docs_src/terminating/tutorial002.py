import typer


def main(username: str):
    if username == "root":
        print("The root user is reserved")
        raise typer.Exit(code=1)
    print(f"New user created: {username}")


if __name__ == "__main__":
    typer.run(main)
