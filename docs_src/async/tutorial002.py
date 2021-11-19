import anyio
import typer


async def main():
    await anyio.sleep(1)
    typer.echo("Hello World")


if __name__ == "__main__":
    typer.run(main)
