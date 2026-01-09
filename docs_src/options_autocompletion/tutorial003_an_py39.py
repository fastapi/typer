import typer
from typing_extensions import Annotated

valid_users = ["Camila", "Carlos", "Sebastian"]


def complete_user(incomplete: str):
    completion = []
    for user in valid_users:
        if user.startswith(incomplete):
            completion.append(user)
    return completion


app = typer.Typer()


@app.command()
def main(
    user: Annotated[
        str, typer.Option(help="The user to say hi to.", autocompletion=complete_user)
    ] = "World",
):
    print(f"Hello {user}")


if __name__ == "__main__":
    app()
