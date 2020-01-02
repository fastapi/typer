In the *First Steps* section you saw how to add help for a CLI app/command by adding it to a function's <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr>.

Here's how that last example looked like:

```Python
{!./src/first_steps/tutorial006.py!}
```

Now we'll add a *help* section to the *CLI options*:

```Python hl_lines="6 7"
{!./src/options/help/tutorial001.py!}
```

We are replacing the default values we had before with `typer.Option()`.

As we no longer have a default value there, the first parameter to `typer.Option()` serves the same purpose of defining that default value.

So, if we had:

```Python
lastname: str = ""
```

now we write:

```Python
lastname: str = typer.Option("")
```

And both forms achieve the same: a *CLI option* with a default value of an empty string (`""`).

And then we can pass the `help` keyword parameter:

```Python
lastname: str = typer.Option("", help="this option does this and that")
```

to create the help for that *CLI option*.

Copy that example from above to a file `main.py`.

Test it:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] NAME

  Say hi to NAME, optionally with a --lastname.

  If --formal is used, say hi very formally.

Options:
  --lastname TEXT         Last name of person to greet.
  --formal / --no-formal  Say hi formally.
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.

// Now you have a help text for the --lastname and --formal CLI options 🎉
```

</div>

## Show default in help

You can tell Typer to show the default value in the help text with `show_default=True`:

```Python hl_lines="4"
{!./src/options/help/tutorial002.py!}
```

And it will show up in the help text:

<div class="termy">

```console
$ python main.py

Hello Wade Wilson

// Show the help
$ python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname TEXT       [default: Wade Wilson]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

!!! tip
    Notice the `[default: Wade Wilson]` in the help text.
