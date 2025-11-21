import asyncio

import trio
import typer

app = typer.Typer()


@app.command()
async def wait_trio(seconds: int):
    await trio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds using trio (default)")


@app.command(async_runner=asyncio.run)
async def wait_asyncio(seconds: int):
    await asyncio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds using asyncio (custom runner)")


if __name__ == "__main__":
    app()
