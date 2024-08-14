# Typer Callback

When you create an `app = typer.Typer()` it works as a group of commands.

And you can create multiple commands with it.

Each of those commands can have their own *CLI parameters*.

But as those *CLI parameters* are handled by each of those commands, they don't allow us to create *CLI parameters* for the main CLI application itself.

But we can use `@app.callback()` for that.

It's very similar to `@app.command()`, but it declares the *CLI parameters* for the main CLI application (before the commands):

```Python hl_lines="25 26 27 28 29 30 31 32"
{!../docs_src/commands/callback/tutorial001.py!}
```

Here we create a `callback` with a `--verbose` *CLI option*.

/// tip

After getting the `--verbose` flag, we modify a global `state`, and we use it in the other commands.

There are other ways to achieve the same, but this will suffice for this example.

///

And as we added a docstring to the callback function, by default it will be extracted and used as the help text.

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// Notice the main help text, extracted from the callback function: "Manage users in the awesome CLI app."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Manage users in the awesome CLI app.

Options:
  --verbose / --no-verbose  [default: False]
  --install-completion      Install completion for the current shell.
  --show-completion         Show completion for the current shell, to copy it or customize the installation.
  --help                    Show this message and exit.

Commands:
  create
  delete

// Check the new top level CLI option --verbose

// Try it normally
$ python main.py create Camila

Creating user: Camila

// And now with --verbose
$ python main.py --verbose create Camila

Will write verbose output
About to create a user
Creating user: Camila
Just created a user

// Notice that --verbose belongs to the callback, it has to go before create or delete ⛔️
$ python main.py create --verbose Camila

Usage: main.py create [OPTIONS] USERNAME
Try "main.py create --help" for help.

Error: No such option: --verbose
```

</div>

## Adding a callback on creation

It's also possible to add a callback when creating the `typer.Typer()` app:

```Python hl_lines="4 5  8"
{!../docs_src/commands/callback/tutorial002.py!}
```

That achieves the same as with `@app.callback()`.

Check it:

<div class="termy">

```console
$ python main.py create Camila

Running a command
Creating user: Camila
```

</div>

## Overriding a callback

If you added a callback when creating the `typer.Typer()` app, it's possible to override it with `@app.callback()`:

```Python hl_lines="11 12 13"
{!../docs_src/commands/callback/tutorial003.py!}
```

Now `new_callback()` will be the one used.

Check it:

<div class="termy">

```console
$ python main.py create Camila

// Notice that the message is the one from new_callback()
Override callback, running a command
Creating user: Camila
```

</div>

## Adding a callback only for documentation

You can also add a callback just to add the documentation in the docstring.

It can be convenient especially if you have several lines of text, as the indentation will be automatically handled for you:

```Python hl_lines="8 9 10 11 12 13 14 15 16"
{!../docs_src/commands/callback/tutorial004.py!}
```

Now the callback will be used mainly to extract the docstring for the help text.

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice all the help text extracted from the callback docstring
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Manage users CLI app.

  Use it with the create command.

  A new user with the given NAME will be created.

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  create

// And it just works as normally
$ python main.py create Camila

Creating user: Camila
```

</div>

## Click Group

If you come from Click, this **Typer** callback is the equivalent of the function in a <a href="https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands" class="external-link" target="_blank">Click Group</a>.

For example:

```Python
import click

@click.group()
def cli():
    pass
```

The original function `cli` would be the equivalent of a Typer callback.

/// note | Technical Details

When using Click, it converts that `cli` variable to a Click `Group` object. And then the original function no longer exists in that variable.

**Typer** doesn't do that, the callback function is not modified, only registered in the `typer.Typer` app. This is intentional, it's part of **Typer**'s design, to allow having editor auto completion and type checks.

///
