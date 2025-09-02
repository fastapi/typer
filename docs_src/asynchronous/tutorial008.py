import asyncio

import anyio
import typer

app = typer.Typer(async_runner=lambda c: anyio.run(lambda: c, backend="asyncio"))


@app.command()
async def wait_anyio(seconds: int):
    await anyio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds using asyncio via anyio")


@app.command()
async def wait_asyncio(seconds: int):
    await asyncio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds using asyncio")


if __name__ == "__main__":
    app()
