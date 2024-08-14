# CLI Options with Help

You already saw how to add a help text for *CLI arguments* with the `help` parameter.

Let's now do the same for *CLI options*:

//// tab | Python 3.7+

```Python hl_lines="7-8"
{!> ../docs_src/options/help/tutorial001_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="6-7"
{!> ../docs_src/options/help/tutorial001.py!}
```

////

The same way as with `typer.Argument()`, we can put `typer.Option()` inside of `Annotated`.

We can then pass the `help` keyword parameter:

```Python
lastname: Annotated[str, typer.Option(help="this option does this and that")] = ""
```

...to create the help for that *CLI option*.

The same way as with `typer.Argument()`, **Typer** also supports the old style using the function parameter default value:

```Python
lastname: str = typer.Option(default="", help="this option does this and that")
```

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
  --help                  Show this message and exit.

// Now you have a help text for the --lastname and --formal CLI options 🎉
```

</div>

## *CLI Options* help panels

The same as with *CLI arguments*, you can put the help for some *CLI options* in different panels to be shown with the `--help` option.

If you have installed Rich as described in the docs for [Printing and Colors](../printing.md){.internal-link target=_blank}, you can set the `rich_help_panel` parameter to the name of the panel you want for each *CLI option*:

//// tab | Python 3.7+

```Python hl_lines="11  17"
{!> ../docs_src/options/help/tutorial002_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8  11"
{!> ../docs_src/options/help/tutorial002.py!}
```

////

Now, when you check the `--help` option, you will see a default panel named "`Options`" for the *CLI options* that don't have a custom `rich_help_panel`.

And below you will see other panels for the *CLI options* that have a custom panel set in the `rich_help_panel` parameter:

<div class="termy">

```console
$ python main.py --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>main.py [OPTIONS] NAME                                </b>
<b>                                                                     </b>
 Say hi to NAME, optionally with a <font color="#A1EFE4"><b>--lastname</b></font>.
 If <font color="#6B9F98"><b>--formal</b></font><font color="#A5A5A1"> is used, say hi very formally.                          </font>

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    name      <font color="#F4BF75"><b>TEXT</b></font>  [default: None] <font color="#A6194C">[required]</font>                   │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--lastname</b></font>                  <font color="#F4BF75"><b>TEXT</b></font>  Last name of person to greet.   │
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                      <font color="#F4BF75"><b>    </b></font>  Show this message and exit.     │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Customization and Utils ─────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--formal</b></font>    <font color="#AE81FF"><b>--no-formal</b></font>      Say hi formally.                     │
<font color="#A5A5A1">│                              [default: no-formal]                 │</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--debug</b></font>     <font color="#AE81FF"><b>--no-debug</b></font>       Enable debugging.                    │
<font color="#A5A5A1">│                              [default: no-debug]                  │</font>
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>

Here we have a custom *CLI options* panel named "`Customization and Utils`".

## Help with style using Rich

In a future section you will see how to use custom markup in the `help` for *CLI options* when reading about [Commands - Command Help](../commands/help.md#rich-markdown-and-markup){.internal-link target=_blank}.

If you are in a hurry you can jump there, but otherwise, it would be better to continue reading here and following the tutorial in order.


## Hide default from help

You can tell Typer to not show the default value in the help text with `show_default=False`:

//// tab | Python 3.7+

```Python hl_lines="5"
{!> ../docs_src/options/help/tutorial003_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="4"
{!> ../docs_src/options/help/tutorial003.py!}
```

////

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
  --help                Show this message and exit.

// Notice there's no [default: Wade Wilson] 🔥
```

</div>

/// note | Technical Details

In Click applications the default values are hidden by default. 🙈

In **Typer** these default values are shown by default. 👀

///

## Custom default string

You can use the same `show_default` to pass a custom string (instead of a `bool`) to customize the default value to be shown in the help text:

//// tab | Python 3.7+

```Python hl_lines="7"
{!> ../docs_src/options/help/tutorial004_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="6"
{!> ../docs_src/options/help/tutorial004.py!}
```

////

And it will be used in the help text:

<div class="termy">

```console
$ python main.py

Hello Wade Wilson

// Show the help
$ python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname TEXT       [default: (Deadpoolio the amazing's name)]
  --help                Show this message and exit.

// Notice how it shows "(Deadpoolio the amazing's name)" instead of the actual default of "Wade Wilson"
```

</div>
