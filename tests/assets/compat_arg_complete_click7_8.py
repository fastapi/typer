import click
import typer
from typer._compat_utils import _get_click_major

app = typer.Typer()


def shell_complete(ctx: click.Context, param: click.Parameter, incomplete: str):
    typer.echo(f"ctx: {ctx.info_name}", err=True)
    typer.echo(f"arg is: {param.name}", err=True)
    typer.echo(f"incomplete is: {incomplete}", err=True)
    if _get_click_major() > 7:
        from click.shell_completion import CompletionItem

        return [CompletionItem("Emma", help="Emma is awesome.")]
    return ["Emma"]


@app.command(context_settings={"auto_envvar_prefix": "TEST"})
def main(name: str = typer.Argument(shell_complete=shell_complete)):
    """
    Say hello.
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
