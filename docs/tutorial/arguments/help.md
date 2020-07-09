In the *First Steps* section you saw how to add help for a CLI app/command by adding it to a function's <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr>.

Here's how that last example looked like:

```Python
{!../docs_src/first_steps/tutorial006.py!}
```

Now that you also know how to use `typer.Argument()`, let's use it to add documentation specific for a *CLI argument*.

## Add a `help` text for a *CLI argument*

You can use the `help` parameter to add a help text for a *CLI argument*:

```Python hl_lines="4"
{!../docs_src/arguments/help/tutorial001.py!}
```

And it will be used in the automatic `--help` option:

<div class="termy">

```console
$ python main.py --help

// Check the section with Arguments below 🚀
Usage: main.py [OPTIONS] NAME

Arguments:
  NAME  The name of the user to greet  [required]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## Combine help text and docstrings

And of course, you can also combine that `help` with the <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr>:

```Python hl_lines="4 5 6 7"
{!../docs_src/arguments/help/tutorial002.py!}
```

And the `--help` option will combine all the information:

<div class="termy">

```console
$ python main.py --help

// Notice that we have the help text from the docstring and also the Arguments 📝
Usage: main.py [OPTIONS] NAME

  Say hi to NAME very gently, like Dirk.

Arguments:
  NAME  The name of the user to greet  [required]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## Help with defaults

If you have a *CLI argument* with a default value, like `"World"`:

```Python hl_lines="4"
{!../docs_src/arguments/help/tutorial003.py!}
```

It will show that default value in the help text:

<div class="termy">

```console
$ python main.py --help

// Notice the [default: World] 🔍
Usage: main.py [OPTIONS] [NAME]

  Say hi to NAME very gently, like Dirk.

Arguments:
  [NAME]  Who to greet  [default: World]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

But you can disable that if you want to, with `show_default=False`:

```Python hl_lines="4"
{!../docs_src/arguments/help/tutorial004.py!}
```

And then it won't show the default value:

<div class="termy">

```console
$ python main.py --help

// Notice the there's no [default: World] now 🔥
Usage: main.py [OPTIONS] [NAME]

  Say hi to NAME very gently, like Dirk.

Arguments:
  [NAME]  Who to greet

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.

  --help                Show this message and exit.
```

</div>

!!! note "Technical Details"
    In Click applications the default values are hidden by default. 🙈

    In **Typer** these default values are shown by default. 👀

## Custom default string

You can use the same `show_default` to pass a custom string (instead of a `bool`) to customize the default value to be shown in the help text:

```Python hl_lines="6"
{!../docs_src/arguments/help/tutorial005.py!}
```

And it will be used in the help text:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  Who to greet  [default: (Deadpoolio the amazing's name)]


Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// See it shows "(Deadpoolio the amazing's name)" instead of the actual default of "Wade Wilson"
```

</div>

## Custom help name (`metavar`)

You can also customize the text used in the generated help text to represent a *CLI argument*.

By default, it will be the same name you declared, in uppercase letters.

So, if you declare it as:

```Python
name: str
```

It will be shown as:

```
NAME
```

But you can customize it with the `metavar` parameter for `typer.Argument()`.

For example, let's say you don't want to have the default of `NAME`, you want to have `username`, in lowercase, and you really want ✨ emojis ✨ everywhere:

```Python hl_lines="4"
{!../docs_src/arguments/help/tutorial006.py!}
```

Now the generated help text will have `✨username✨` instead of `NAME`:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] ✨username✨

Arguments:
  ✨username✨  [default: World]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## Hide a *CLI argument* from the help text

If you want, you can make a *CLI argument* **not** show up in the `Arguments` section in the help text.

You will probably not want to do this normally, but it's possible:

```Python hl_lines="4"
{!../docs_src/arguments/help/tutorial007.py!}
```

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice there's no Arguments section at all 🔥
Usage: main.py [OPTIONS] [NAME]

  Say hi to NAME very gently, like Dirk.

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

!!! info
    Have in mind that the *CLI argument* will still show up in the first line with `Usage`.

    But it won't show up in the main help text under the `Arguments` section.

### Help text for *CLI arguments* in Click

Click itself doesn't support adding help for *CLI arguments*, and it doesn't generate help for them as in the "`Arguments:`" sections in the examples above.

Not supporting `help` in *CLI arguments* is an intentional <a href="https://click.palletsprojects.com/en/7.x/documentation/#documenting-arguments" class="external-link" target="_blank">design decision in Click</a>:

> This is to follow the general convention of Unix tools of using arguments for only the most necessary things, and to document them in the command help text by referring to them by name.

So, in Click applications, you are expected to write all the documentation for *CLI arguments* by hand in the <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr>.

---

Nevertheless, **Typer supports `help` for *CLI arguments***. ✨ 🤷‍♂

**Typer** doesn't follow that convention and instead supports `help` to make it easier to have consistent help texts with a consistent format for your CLI programs. 🎨

This is also to help you create CLI programs that are ✨ awesome ✨ *by default*. With very little code.

If you want to keep Click's convention in a **Typer** app, you can do it with the `hidden` parameter as described above.

!!! note "Technical Details"
    To support `help` in *CLI arguments* **Typer** does a lot of internal work in its own sub-classes of Click's internal classes.
