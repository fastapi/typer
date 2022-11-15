import reigns
import towns

import typer

app = typer.Typer()
app.add_typer(reigns.app, name="reigns")
app.add_typer(towns.app, name="towns")

if __name__ == "__main__":
    app()
