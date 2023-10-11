import anyio
import typer

app = typer.Typer()


@app.command()
async def main():
    await anyio.sleep(1)
    typer.echo("Hello World")


if __name__ == "__main__":
    app()
