import typer


def main(user_info: dict = typer.Option()):
    print(f"Name: {user_info.get('name', 'Unknown')}")
    print(f"User attributes: {sorted(user_info.keys())}")


if __name__ == "__main__":
    typer.run(main)
