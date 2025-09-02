import asyncio

import trio
import typer

app = typer.Typer()


@app.command()
async def wait_trio(seconds: int):
    await trio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds using trio (default)")


@app.callback(async_runner=lambda c: asyncio.run(c))
async def wait_asyncio(seconds: int):
    await asyncio.sleep(seconds)
    typer.echo(
        f"Waited for {seconds} seconds before running command using asyncio (customized)"
    )


if __name__ == "__main__":
    app()
