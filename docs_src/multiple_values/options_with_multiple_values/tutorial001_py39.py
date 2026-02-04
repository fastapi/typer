"""
This example shows how to define a Typer option that accepts multiple values
using a tuple type hint.

The --user option expects exactly three values, in this order:
1. username (str)
2. coins (int)
3. is_wizard (bool)

Example usage:
python tutorial001_py39.py --user Harry 100 true
"""
import typer

app = typer.Typer()


@app.command()
def main(user: tuple[str, int, bool] = typer.Option((None, None, None))):
    username, coins, is_wizard = user
    if not username:
        print("No user provided")
        raise typer.Abort()
    print(f"The username {username} has {coins} coins")
    if is_wizard:
        print("And this user is a wizard!")


if __name__ == "__main__":
    app()
