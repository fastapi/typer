import asyncio

import typer

app = typer.Typer()


@app.command()
async def wait(seconds: int):
    await asyncio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds")


if __name__ == "__main__":
    app()
