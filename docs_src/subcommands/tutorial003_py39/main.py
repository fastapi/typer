import typer

import items
import lands
import users

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")
app.add_typer(lands.app, name="lands")

if __name__ == "__main__":
    app()
