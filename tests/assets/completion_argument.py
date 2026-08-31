import typer
from typer import _click

app = typer.Typer()


def shell_complete(ctx: _click.Context, param: _click.Parameter, incomplete: str):
    typer.echo(f"ctx: {ctx.info_name}", err=True)
    typer.echo(f"arg is: {param.name}", err=True)
    typer.echo(f"incomplete is: {incomplete}", err=True)
    return ["Emma"]


@app.command(context_settings={"auto_envvar_prefix": "TEST"})
def main(name: str = typer.Argument(shell_complete=shell_complete)):
    """
    Say hello.
    """


if __name__ == "__main__":
    app()
