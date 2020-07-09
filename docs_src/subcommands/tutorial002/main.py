import typer

app = typer.Typer()
items_app = typer.Typer()
app.add_typer(items_app, name="items")
users_app = typer.Typer()
app.add_typer(users_app, name="users")


@items_app.command("create")
def items_create(item: str):
    typer.echo(f"Creating item: {item}")


@items_app.command("delete")
def items_delete(item: str):
    typer.echo(f"Deleting item: {item}")


@items_app.command("sell")
def items_sell(item: str):
    typer.echo(f"Selling item: {item}")


@users_app.command("create")
def users_create(user_name: str):
    typer.echo(f"Creating user: {user_name}")


@users_app.command("delete")
def users_delete(user_name: str):
    typer.echo(f"Deleting user: {user_name}")


if __name__ == "__main__":
    app()
