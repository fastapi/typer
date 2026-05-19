import typer

app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def main(ctx: typer.Context):
    for extra_arg in ctx.args:
        print(f"Got extra arg: {extra_arg}")


if __name__ == "__main__":
    app()
