import typer


def main(user_name: str = typer.Option(..., "--name")):
    print(f"Hello {user_name}")


if __name__ == "__main__":
    typer.run(main)
