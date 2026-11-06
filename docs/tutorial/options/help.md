# CLI Options with Help

You already saw how to add a help text for *CLI arguments* with the `help` parameter.

Let's now do the same for *CLI options*:

{* docs_src/options/help/tutorial001_an_py310.py hl[11:12] *}

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
$ uv run python main.py --help

Usage: main.py [OPTIONS] {name}

  Say hi to 'name', optionally with a --lastname.

  If --formal is used, say hi very formally.

Arguments:
  name  [required]

Options:
  --lastname <str>        Last name of person to greet.
  --formal / --no-formal  Say hi formally.  [default: no-formal]
  --help                  Show this message and exit.

// Now you have a help text for the --lastname and --formal CLI options 🎉
```

</div>

## *CLI Options* help panels

The same as with *CLI arguments*, you can put the help for some *CLI options* in different panels to be shown with the `--help` option.

Using Rich, you can set the `rich_help_panel` parameter to the name of the panel you want for each *CLI option*:

{* docs_src/options/help/tutorial002_an_py310.py hl[15,21] *}

Now, when you check the `--help` option, you will see a default panel named "`Options`" for the *CLI options* that don't have a custom `rich_help_panel`.

And below you will see other panels for the *CLI options* that have a custom panel set in the `rich_help_panel` parameter:

<div class="termy">

```console
$ uv run python main.py --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>main.py [OPTIONS] {name}                                </b>
<b>                                                                     </b>
 Say hi to 'name', optionally with a <font color="#A1EFE4"><b>--lastname</b></font>.
 If <font color="#6B9F98"><b>--formal</b></font><font color="#A5A5A1"> is used, say hi very formally.                          </font>

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    name      <font color="#F4BF75"><b>&lt;str&gt;</b></font>  <font color="#A6194C">[required]</font>                                  │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--lastname</b></font>                  <font color="#F4BF75"><b>&lt;str&gt;</b></font>  Last name of person to greet.  │
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

## Align option and argument columns across panels

By default, each panel sizes its own columns, so the columns don't line up between panels.

You can make `typer.Typer()` give every panel the same fixed column widths with `align_panel_columns=True`:

{* docs_src/options/help/tutorial005_an_py310.py hl[5] *}

Now *CLI arguments*, *CLI options* and every *CLI options* panel share the same grid. The names of the *CLI arguments* line up with the long names of the *CLI options*, and the required marker (`*`) column is shared too, reserved whenever any *CLI argument* or *CLI option* is required.

Here the command has a required *CLI argument* and an optional one, one panel has only short options, another mixes short and long options, and the last has only long options:

<div class="termy">

```console
$ uv run python main.py --help

 Usage: main.py [OPTIONS] {source} [dest]

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *  source                <str>  Source path. [required]                      │
│    dest                  <str>  Destination path.                            │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│    --help                       Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Short ──────────────────────────────────────────────────────────────────────╮
│                  -a             Short flag.                                  │
│                  -b      <str>  Short value.                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Mixed ──────────────────────────────────────────────────────────────────────╮
│    --mixed-long  -m      <str>  Mixed value.                                 │
│    --mixed-flag  -f             Mixed flag.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Long ───────────────────────────────────────────────────────────────────────╮
│    --alpha               <str>  Long value.                                  │
│    --beta                       Long flag.                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

</div>

## A complete alignment example

The following example puts it all together. It has a required *CLI argument*, an optional one and a variadic one, plus *CLI options* covering every shape that changes the help layout: short-only, long-only, an alias, mixed, negative long-only, negative short-only, negative long and short, a custom `metavar`, an enum, a numeric range, a count option, a default, a custom default string, an environment variable, and a hidden option:

{* docs_src/options/help/tutorial006_an_py310.py hl[7] *}

Even with all of those, every panel shares one grid, so the argument names, option long names, short names, negative names and metavars all line up, and the hidden option does not appear:

<div class="termy">

```console
$ uv run python main.py --help

 Usage: main.py [OPTIONS] {source} [dest] [extras]...

 Build the project.

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────╮
│ *  source                                <str>                  Source directory. [required]     │
│    dest                                  <str>                  Destination directory.           │
│                                                                 [default: dist]                  │
│    extras                                <str>                  Extra files.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│    --help                                                       Show this message and exit.      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Required ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --token                               <str>                  API token. [required]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Basic flags ────────────────────────────────────────────────────────────────────────────────────╮
│                     -v                                          Verbose.                         │
│    --alpha,--aleph                       <str>                  Long value with an alias.        │
│    --mixed-long     -m                   <str>                  Mixed value.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Negative flags ─────────────────────────────────────────────────────────────────────────────────╮
│    --force          -f  --no-force                              Force. [default: no-force]       │
│                     -p               -P                         Pretty. [default: P]             │
│    --formal             --no-formal                             Formal. [default: no-formal]     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Values ─────────────────────────────────────────────────────────────────────────────────────────╮
│    --path                                PATH                   Output path. [default: .]        │
│    --color                               <red|green>            Color. [default: red]            │
│    --level                               <int range> [0<=x<=5]  Level. [default: 1]              │
│    --count          -c                   <int>                  Count. [default: 0]              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Defaults ───────────────────────────────────────────────────────────────────────────────────────╮
│    --timeout                             <int>                  Timeout. [default: 30]           │
│    --mode                                <str>                  Mode. [default: (auto)]          │
│    --home                                <str>                  Home. [env var: HOME]            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```

</div>

## Help with style using Rich

In a future section you will see how to use custom markup in the `help` for *CLI options* when reading about [Commands - Command Help](../commands/help.md#rich-markdown-and-markup).

If you are in a hurry you can jump there, but otherwise, it would be better to continue reading here and following the tutorial in order.


## Hide default from help

You can tell Typer to not show the default value in the help text with `show_default=False`:

{* docs_src/options/help/tutorial003_an_py310.py hl[9] *}

And it will no longer show the default value in the help text:

<div class="termy">

```console
$ uv run python main.py

Hello Wade Wilson

// Show the help
$ uv run python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname <str>
  --help                Show this message and exit.

// Notice there's no [default: Wade Wilson] 🔥
```

</div>

## Custom default string

You can use the same `show_default` to pass a custom string (instead of a `bool`) to customize the default value to be shown in the help text:

{* docs_src/options/help/tutorial004_an_py310.py hl[11] *}

And it will be used in the help text:

<div class="termy">

```console
$ uv run python main.py

Hello Wade Wilson

// Show the help
$ uv run python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname <str>      [default: (Deadpoolio the amazing's name)]
  --help                Show this message and exit.

// Notice how it shows "(Deadpoolio the amazing's name)" instead of the actual default of "Wade Wilson"
```

</div>
