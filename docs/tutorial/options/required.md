# Required CLI Options

We said before that *by default*:

* *CLI options* are **optional**
* *CLI arguments* are **required**

Well, that's how they work *by default*, and that's the convention in many CLI programs and systems.

But if you really want, you can change that.

To make a *CLI option* required, you can put `typer.Option()` inside of `Annotated` and leave the parameter without a default value.

Let's make `--lastname` a required *CLI option*:

//// tab | Python 3.8+

```Python hl_lines="5"
{!> ../docs_src/options/required/tutorial001_an.py!}
```

////

The same way as with `typer.Argument()`, the old style of using the function parameter default value is also supported, in that case you would just not pass anything to the `default` parameter.

//// tab | Python 3.8+ non-Annotated

```Python hl_lines="4"
{!> ../docs_src/options/required/tutorial001.py!}
```

////

Or you can explictily pass `...` to `typer.Option(default=...)`:

//// tab | Python 3.8+ non-Annotated

```Python hl_lines="4"
{!> ../docs_src/options/required/tutorial002.py!}
```

////

/// info

If you hadn't seen that `...` before: it is a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">part of Python and is called "Ellipsis"</a>.

///

That will tell **Typer** that it's still a *CLI option*, but it doesn't have a default value, and it's required.

/// tip

Again, prefer to use the `Annotated` version if possible. That way your code will mean the same in standard Python and in **Typer**.

///

And test it:

<div class="termy">

```console
// Pass the NAME CLI argument
$ python main.py Camila

// We didn't pass the now required --lastname CLI option
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing option '--lastname'.

// Now update it to pass the required --lastname CLI option
$ python main.py Camila --lastname Gutiérrez

Hello Camila Gutiérrez

// And if you check the help
$ python main.py --help

Usage: main.py [OPTIONS] NAME

Options:
  --lastname TEXT       [required]
  --help                Show this message and exit.

// It now tells you that --lastname is required 🎉
```

</div>
