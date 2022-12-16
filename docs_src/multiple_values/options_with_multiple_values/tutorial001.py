from typing import Tuple

import typer


def main(user: Tuple[str, int, bool] = typer.Option((None, None, None))):
    username, coins, is_wizard = user
    if not username:
        print("No user provided")
        raise typer.Abort()
    print(f"The username {username} has {coins} coins")
    if is_wizard:
        print("And this user is a wizard!")


if __name__ == "__main__":
    typer.run(main)
