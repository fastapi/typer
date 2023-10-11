import typer

app = typer.Typer()


@app.command()
async def wait(seconds: int):
    import trio
    await trio.sleep(seconds)
    typer.echo(f"Waited for {seconds} seconds")


if __name__ == "__main__":
    app()
