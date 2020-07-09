You already saw how to add a help text for *CLI arguments* with the `help` parameter.

Let's now do the same for *CLI options*:

```Python hl_lines="6 7"
{!../docs_src/options/help/tutorial001.py!}
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

Arguments:
  NAME  [required]

Options:
  --lastname TEXT         Last name of person to greet. [default: ]
  --formal / --no-formal  Say hi formally.  [default: False]
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.

// Now you have a help text for the --lastname and --formal CLI options 🎉
```

</div>

## Hide default from help

You can tell Typer to not show the default value in the help text with `show_default=False`:

```Python hl_lines="4"
{!../docs_src/options/help/tutorial002.py!}
```

And it will no longer show the default value in the help text:

<div class="termy">

```console
$ python main.py

Hello Wade Wilson

// Show the help
$ python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname TEXT
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Notice there's no [default: Wade Wilson] 🔥
```

</div>

!!! note "Technical Details"
    In Click applications the default values are hidden by default. 🙈

    In **Typer** these default values are shown by default. 👀
