# Version CLI Option, `is_eager`

You could use a callback to implement a `--version` *CLI option*.

It would show the version of your CLI program and then it would terminate it. Even before any other *CLI parameter* is processed.

## First version of `--version`

Let's see a first version of how it could look like:

//// tab | Python 3.8+

```Python hl_lines="9-12  17-19"
{!> ../docs_src/options/version/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8-11  16-18"
{!> ../docs_src/options/version/tutorial001.py!}
```

////

/// tip

Notice that we don't have to get the `typer.Context` and check for `ctx.resilient_parsing` for completion to work, because we only print and modify the program when `--version` is passed, otherwise, nothing is printed or changed from the callback.

///

If the `--version` *CLI option* is passed, we get a value `True` in the callback.

Then we can print the version and raise `typer.Exit()` to make sure the program is terminated before anything else is executed.

We also declare the explicit *CLI option* name `--version`, because we don't want an automatic `--no-version`, it would look awkward.

Check it:

<div class="termy">

```console
$ python main.py --help

// We get a --version, and don't get an awkward --no-version 🎉
Usage: main.py [OPTIONS]

Options:
  --version
  --name TEXT
  --help                Show this message and exit.


// We can call it normally
$ python main.py --name Camila

Hello Camila

// And we can get the version
$ python main.py --version

Awesome CLI Version: 0.1.0

// Because we exit in the callback, we don't get a "Hello World" message after the version 🚀
```

</div>

## Previous parameters and `is_eager`

But now let's say that the `--name` *CLI option* that we declared before `--version` is required, and it has a callback that could exit the program:

//// tab | Python 3.8+

```Python hl_lines="15-17  22-24"
{!> ../docs_src/options/version/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="14-16  21-23"
{!> ../docs_src/options/version/tutorial002.py!}
```

////

Then our CLI program could not work as expected in some cases as it is *right now*, because if we use `--version` after `--name` then the callback for `--name` will be processed before and we can get its error:

<div class="termy">

```console
$ python main.py --name Rick --version

Only Camila is allowed
Aborted!
```

</div>

/// tip

We don't have to check for `ctx.resilient_parsing` in the `name_callback()` for completion to work, because we are not using `typer.echo()`, instead we are raising a `typer.BadParameter`.

///

/// note | Technical Details

`typer.BadParameter` prints the error to "standard error", not to "standard output", and because the completion system only reads from "standard output", it won't break completion.

///

/// info

If you need a refresher about what is "standard output" and "standard error" check the section in [Printing and Colors: "Standard Output" and "Standard Error"](../printing.md#standard-output-and-standard-error){.internal-link target=_blank}.

///

### Fix with `is_eager`

For those cases, we can mark a *CLI parameter* (a *CLI option* or *CLI argument*) with `is_eager=True`.

That will tell **Typer** (actually Click) that it should process this *CLI parameter* before the others:

//// tab | Python 3.8+

```Python hl_lines="23-26"
{!> ../docs_src/options/version/tutorial003_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="22-24"
{!> ../docs_src/options/version/tutorial003.py!}
```

////

Check it:

<div class="termy">

```console
$ python main.py --name Rick --version

// Now we only get the version, and the name is not used
Awesome CLI Version: 0.1.0
```

</div>
