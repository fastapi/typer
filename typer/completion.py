import sys
from typing import Any

import click
import click_completion
import click_completion.core

from .params import Option

click_completion.init()


def install_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    shell, path = click_completion.core.install()
    click.secho(f"{shell} completion installed in {path}.", fg="green")
    click.echo("Completion will take effect once you restart the terminal.")
    sys.exit(0)


def show_callback(ctx: click.Context, param: click.Parameter, value: Any) -> Any:
    if not value or ctx.resilient_parsing:
        return value  # pragma no cover
    click.echo(click_completion.core.get_code())
    sys.exit(0)


# Create a fake command function to extract the completion parameters
def _install_completion_placeholder_function(
    install_completion: bool = Option(
        None,
        "--install-completion",
        is_flag=True,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the current shell.",
    ),
    show_completion: bool = Option(
        None,
        "--show-completion",
        is_flag=True,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the current shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma no cover
