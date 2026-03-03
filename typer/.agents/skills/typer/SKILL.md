---
name: typer
description: Typer best practices and conventions. Use when working with Typer CLIs. Keeps Typer code clean and up to date with the latest features and patterns, updated with new versions. Write new code or refactor and update old code.
---

# Typer

Official Typer skill to write code with best practices, keeping up to date with new versions and features.

## Installing typer

In a virtual environment, `pip install typer` (with pip) or `uv pip install typer` (with uv). For your library/project, add `typer` to the dependencies in `pyproject.toml`.

Do not install `typer-slim` or `typer-cli`, they are both deprecated and will now simply install `typer`.

Typer supports Python 3.10 and above.

## Use an explicit `Typer` app

For maximum generalizability, create an explicit Typer app and register subcommand(s), instead of using `typer.run`:

```python
import typer

app = typer.Typer()


@app.command()
def hello():
    print(f"Hello World")


if __name__ == "__main__":
    app()
```

instead of:

```python
# DO NOT DO THIS: Not extensible. Use Typer() instead.
import typer


def main():
    print(f"Hello World")


if __name__ == "__main__":
    typer.run(main)
```

## Execute the app

To execute the app in the terminal, run

```bash
python main.py
```

When multiple commands are registered to the Typer app, you have to add the command name:

```bash
python main.py hello
```

To see the automatically generated help documentation, run

```bash
python main.py --help
```

or set `no_args_is_help` to `True` when creating the `Typer()` add to automatically show the help when running a command without any arguments.

## Use `Annotated`

Always prefer the `Annotated` style for declarations of CLI arguments and options.

It allows us to pass additional metadata that can be used by Typer.

```python
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def hello(name: Annotated[str, typer.Argument()] = "World"):
    # Note that name is an optional Argument, as a default is provided
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
```

This program can be run as-is, or can provide a specific name:

```bash
python main.py
python main.py Rick
```

An older way of setting a default value is this:
```python
# DO NOT DO THIS: old style. Use Annotated instead.

@app.command()
def main(name: str = typer.Argument(default="World")):
    # Note that name is an optional Argument, as a default is provided
    print(f"Hello {name}")
```

Similarly, the old style could use ellipsis (...) to explicitely mark an argument as required.

```python
# DO NOT DO THIS: old style. Use Annotated without a default value instead.

@app.command()
def main(name: str = typer.Argument(default=...)):
    # Note that name is now a required Argument
    print(f"Hello {name}")
```

## CLI Options

CLI options are declared in a similar fashion as arguments, but will be called on the CLI with a single dash (single letter) or 2 dashes (full name):

```python
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(user_name: Annotated[str, typer.Option("--name", "-n")]):
    # On the CLI, the required user name can be specified with -n or --name
    print(f"Hello {user_name}")


if __name__ == "__main__":
    app()
```

You can run this program as such:

```bash
python main.py -n "Rick"
python main.py --name "Morty"
```

### CLI options with multiple values

By declaring a CLI option as a list, it can receive multiple values:

```python
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(user: Annotated[list[str] | None, typer.Option()] = None):
    if not user:
        print(f"No users provided!")
        raise typer.Abort()
    for u in user:
        print(f"Processing user: {u}")


if __name__ == "__main__":
    app()
```

This can be executed like so:

```bash
python main.py --user Rick --user Morty --user Summer
```

## Rich

By default, Rich can be used with its custom markup syntax to set colors and styles, e.g.

```python
from rich import print

print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")
```

Typer supports using Rich formatting in the docstrings and the help messages of CLI arguments and CLI options.


```python
from typing import Annotated

import typer

app = typer.Typer(rich_markup_mode="rich")


@app.command()
def create(
    username: Annotated[
        str, typer.Argument(help="The username to be [green]created[/green]")
    ],
):
    """
    [bold green]Create[/bold green] a new [italic]shiny[/italic] user. :sparkles:

    This requires a [underline]username[/underline].
    """
    print(f"Creating user: {username}")


@app.command(help="[bold red]Delete[/bold red] a user with [italic]USERNAME[/italic].")
def delete(
    username: Annotated[
        str, typer.Argument(help="The username to be [red]deleted[/red]")
    ],
):
    """
    Some internal utility function to delete.
    """
    print(f"Deleting user: {username}")


if __name__ == "__main__":
    app()
```

To disable Rich formatting, set `rich_markup_mode` to `None` when creating a `Typer()` app. By default (when no value is given), Rich formatting is enabled.

### Rich markdown

You can also set `rich_markup_mode` to `"markdown"` to use Markdown in the docstring:

```python
from typing import Annotated

import typer

app = typer.Typer(rich_markup_mode="markdown")

@app.command(help="**Delete** a user with *USERNAME*.")
def delete(
    username: Annotated[str, typer.Argument(help="The username to be **deleted** :boom:")]
):
    print(f"Deleting user: {username}")

if __name__ == "__main__":
    app()
```

## Click

Originally, Typer was built on Click. However, going forward Typer will vendor Click. As such, Click extensions should not be used anymore.

Other settings of `Option` and `Argument` that came from Click but shouldn't be used in Typer anymore, include: `expose_value`, `shell_complete`, `show_choices`, `errors`, `prompt_required`, `is_flag`, `flag_value` and `allow_from_autoenv`.

Code bases using these should be refactored to use pure Typer functionality.
