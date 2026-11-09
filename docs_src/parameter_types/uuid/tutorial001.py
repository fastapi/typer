from uuid import UUID

import typer

app = typer.Typer()


@app.command()
def main(user_id: UUID):
    print(f"User ID is {user_id}")
    print(f"UUID version is: {user_id.version}")


if __name__ == "__main__":
    app()
