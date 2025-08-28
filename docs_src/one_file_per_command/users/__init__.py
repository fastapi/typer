import typer

from .add import app as add_app
from .delete import app as delete_app

app = typer.Typer()

app.add_typer(add_app)
app.add_typer(delete_app)
