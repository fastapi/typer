The same as before, you can add help for the commands in the docstrings and the *CLI options*.

And the `typer.Typer()` application receives a parameter `help` that you can pass with the main help text for your CLI program:

```Python hl_lines="3  8 9 10  20  23 24 25 26 27  39  42 43 44 45 46  55 56 57"
{!../docs_src/commands/help/tutorial001.py!}
```

Check it:

<div class="termy">

```console
// Check the new help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Awesome CLI user manager.

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  create      Create a new user with USERNAME.
  delete      Delete a user with USERNAME.
  delete-all  Delete ALL users in the database.
  init        Initialize the users database.

// Now the commands have inline help 🎉

// Check the help for create
$ python main.py create --help

Usage: main.py create [OPTIONS] USERNAME

  Create a new user with USERNAME.

Options:
  --help  Show this message and exit.

// Check the help for delete
$ python main.py delete --help

Usage: main.py delete [OPTIONS] USERNAME

  Delete a user with USERNAME.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for delete-all
$ python main.py delete-all --help

Usage: main.py delete-all [OPTIONS]

  Delete ALL users in the database.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for init
$ python main.py init --help

Usage: main.py init [OPTIONS]

  Initialize the users database.

Options:
  --help  Show this message and exit.
```

</div>

!!! tip
    `typer.Typer()` receives several other parameters for other things, we'll see that later.

    You will also see how to use "Callbacks" later, and those include a way to add this same help message in a function docstring.

## Overwrite command help

You will probably be better adding the help text as a docstring to your functions, but if for some reason you wanted to overwrite it, you can use the `help` function argument passed to `@app.command()`:

```Python hl_lines="6  14"
{!../docs_src/commands/help/tutorial002.py!}
```

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// Notice it uses the help passed to @app.command()
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy
                        it or customize the installation.
  --help                Show this message and exit.

Commands:
  create  Create a new user with USERNAME.
  delete  Delete a user with USERNAME.

// It uses "Create a new user with USERNAME." instead of "Some internal utility function to create."
```

</div>

## Docstring with Markdown and Markup

If you have **Rich** installed as described in [Printing and Colors](../printing.md){.internal-link target=_blank}, you can configure your app to enable using rich text in the docstring with the parameter `rich_markup_mode`.

!!! info
    By default, `rich_markup_mode` is `None`, which disables any rich text formatting for the docstring.

### Rich Markup

If you set `rich_markup_mode="rich"` when creating the `typer.Typer()` app, you will be able to use <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">Rich Console Markup</a> in the docstring, and even in the help for the arguments and options:

```Python hl_lines="3  9  13-15  20  22  24"
{!../docs_src/commands/help/tutorial003.py!}
```

With that, you can use <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">Rich Console Markup</a> to format the text in the docstring for the command `create`, make the word "`create`" bold and green, and even use an <a href="https://rich.readthedocs.io/en/stable/markup.html#emoji" class="external-link" target="_blank">emoji</a>.

You can also use markup in the help for the `username` CLI Argument.

And the same as before, the help text overwritten for the command `delete` can also use Rich Markup, the same in the CLI Argument and CLI Option.

If you run the program and check the help, you will see that **Typer** uses **Rich** internally to format the help.

Check the help for the `create` command:

<div class="termy">

```console
$ python main.py create --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>tutorial003.py create [OPTIONS] USERNAME                     </b>
<b>                                                                     </b>
 <font color="#A6E22E"><b>Create</b></font> a new <i>shinny</i> user. ✨
 This requires a <font color="#A5A5A1"><u style="text-decoration-style:single">username</u></font><font color="#A5A5A1">.                                           </font>

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    username      <font color="#F4BF75"><b>TEXT</b></font>  The username to be <font color="#A6E22E">created</font>               │
<font color="#A5A5A1">│                          [default: None]                          │</font>
<font color="#A5A5A1">│                          </font><font color="#A6194C">[required]                </font>               │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>          Show this message and exit.                       │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>

And check the help for the `delete` command:

<div class="termy">

```console
$ python main.py delete --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>tutorial003.py delete [OPTIONS] USERNAME                     </b>
<b>                                                                     </b>
 <font color="#F92672"><b>Delete</b></font> a user with <i>USERNAME</i>.

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    username      <font color="#F4BF75"><b>TEXT</b></font>  The username to be <font color="#F92672">deleted</font>               │
<font color="#A5A5A1">│                          [default: None]                          │</font>
<font color="#A5A5A1">│                          </font><font color="#A6194C">[required]                </font>               │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--force</b></font>    <font color="#AE81FF"><b>--no-force</b></font>      Force the <font color="#F92672"><b>deletion</b></font> 💥                  │
<font color="#A5A5A1">│                            [default: no-force]                    │</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                     Show this message and exit.            │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>


### Rich Markown

If you set `rich_markup_mode="markdown"` when creating the `typer.Typer()` app, you will be able to use Markdown in the docstring:

```Python hl_lines="3  7  9-14  19  21-22"
{!../docs_src/commands/help/tutorial004.py!}
```

With that, you can use Markdown to format the text in the docstring for the command `create`, make the word "`create`" bold, show a list of items, and even use an <a href="https://rich.readthedocs.io/en/stable/markup.html#emoji" class="external-link" target="_blank">emoji</a>.

And the same as before, the help text overwritten for the command `delete` can also use Markdown.

Check the help for the `create` command:

<div class="termy">

```console
$ python main.py create --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>tutorial004.py create [OPTIONS] USERNAME                     </b>
<b>                                                                     </b>
 <b>Create</b> a new <i>shinny</i> user. ✨

 <font color="#F4BF75"><b> • </b></font><font color="#A5A5A1">Create a username                                                </font>
 <font color="#F4BF75"><b> • </b></font><font color="#A5A5A1">Show that the username is created                                </font>

 <font color="#F4BF75">───────────────────────────────────────────────────────────────────</font>
 Learn more at the <font color="#44919F">Typer docs website</font>

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    username      <font color="#F4BF75"><b>TEXT</b></font>  The username to be <b>created</b>               │
<font color="#A5A5A1">│                          [default: None]                          │</font>
<font color="#A5A5A1">│                          </font><font color="#A6194C">[required]                              </font> │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>          Show this message and exit.                       │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>

And the same for the `delete` command:

<div class="termy">

```console
$ python main.py delete --help

<b> </b><font color="#F4BF75"><b>Usage: </b></font><b>tutorial004.py delete [OPTIONS] USERNAME                     </b>
<b>                                                                     </b>
 <b>Delete</b> a user with <i>USERNAME</i>.

<font color="#A5A5A1">╭─ Arguments ───────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#F92672">*</font>    username      <font color="#F4BF75"><b>TEXT</b></font>  The username to be <b>deleted</b>               │
<font color="#A5A5A1">│                          [default: None]                          │</font>
<font color="#A5A5A1">│                          </font><font color="#A6194C">[required]                              </font> │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
<font color="#A5A5A1">╭─ Options ─────────────────────────────────────────────────────────╮</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--force</b></font>    <font color="#AE81FF"><b>--no-force</b></font>      Force the <b>deletion</b> 💥                  │
<font color="#A5A5A1">│                            [default: no-force]                    │</font>
<font color="#A5A5A1">│ </font><font color="#A1EFE4"><b>--help</b></font>                     Show this message and exit.            │
<font color="#A5A5A1">╰───────────────────────────────────────────────────────────────────╯</font>
```

</div>

!!! info
    Notice that in Markdown you cannot define colors. For colors you might prefer to use Rich markup.
