from uuid import UUID

import typer


def main(user_id: UUID):
    typer.echo(f"USER_ID is {user_id}")
    typer.echo(f"UUID version is: {user_id.version}")


if __name__ == "__main__":
    typer.run(main)
