import typer

app = typer.Typer()
remote_app = typer.Typer()


@remote_app.command()
def add(branch=typer.Argument(...), url=typer.Argument(...)):
    print(f"\nAdding remote {branch} with url {url}")


@remote_app.callback(invoke_without_command=True)
def remote(ctx: typer.Context):
    """Adding a remote"""
    if ctx.invoked_subcommand is None:
        print(
            "\nThis is the remote main command. "
            "You can also use the 'add' sub-command."
        )


app.add_typer(remote_app, name="remote")


if __name__ == "__main__":
    app()
