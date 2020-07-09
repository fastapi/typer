import items
import lands
import typer
import users

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(items.app, name="items")
app.add_typer(lands.app, name="lands")

if __name__ == "__main__":
    app()
