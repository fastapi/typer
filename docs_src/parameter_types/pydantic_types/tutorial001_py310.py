import typer
from pydantic import AnyHttpUrl

app = typer.Typer()


@app.command()
def main(url_arg: AnyHttpUrl):
    typer.echo(f"url_arg: {url_arg}")


if __name__ == "__main__":
    app()
