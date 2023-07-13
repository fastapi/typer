import asyncio

import typer

app = typer.Typer()


@app.command("sync")
def command_sync():
    print("Hello Sync World")


@app.command("async")
async def command_async():
    await asyncio.sleep(0)
    print("Hello Async World")


if __name__ == "__main__":
    app()
