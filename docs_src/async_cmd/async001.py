import asyncio

import typer

app = typer.Typer()


async def main():
    await asyncio.sleep(0)
    print("Hello Async World")


if __name__ == "__main__":
    typer.run(main)
