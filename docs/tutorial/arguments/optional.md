# Optional CLI Arguments

We said before that *by default*:

* *CLI options* are **optional**
* *CLI arguments* are **required**

Again, that's how they work *by default*, and that's the convention in many CLI programs and systems.

But you can change that.

In fact, it's very common to have **optional** *CLI arguments*, it's way more common than having **required** *CLI options*.

As an example of how it could be useful, let's see how the `ls` CLI program works.

<div class="termy">

```console
// If you just type
$ ls

// ls will "list" the files and directories in the current directory
typer  tests  README.md  LICENSE

// But it also receives an optional CLI argument
$ ls ./tests/

// And then ls will list the files and directories inside of that directory from the CLI argument
__init__.py  test_tutorial
```

</div>

## An alternative *CLI argument* declaration

In the [First Steps](../first-steps.md#add-a-cli-argument){.internal-link target=_blank} you saw how to add a *CLI argument*:

```Python hl_lines="4"
{!../docs_src/first_steps/tutorial002.py!}
```

Now let's see an alternative way to create the same *CLI argument*:


```Python hl_lines="5"
{!> ../docs_src/arguments/optional/tutorial001_an.py!}
```

/// info

Typer added support for `Annotated` (and started recommending it) in version 0.9.0.

If you have an older version, you would get errors when trying to use `Annotated`.

Make sure you upgrade the Typer version to at least 0.9.0 before using `Annotated`.

///

Before, you had this function parameter:

```Python
name: str
```

And now we wrap it with `Annotated`:

```Python
name: Annotated[str]
```

Both of these versions mean the same thing, `Annotated` is part of standard Python and is there for this.

But the second version using `Annotated` allows us to pass additional metadata that can be used by **Typer**:

```Python
name: Annotated[str, typer.Argument()]
```

Now we are being explicit that `name` is a *CLI argument*. It's still a `str` and it's still required (it doesn't have a default value).

All we did there achieves the same thing as before, a **required** *CLI argument*:

<div class="termy">

```console
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.
```

</div>

It's still not very useful, but it works correctly.

And being able to declare a **required** *CLI argument* using

```Python
name: Annotated[str, typer.Argument()]
```

...that works exactly the same as

```Python
name: str
```

...will come handy later.

## Make an optional *CLI argument*

Now, finally what we came for, an optional *CLI argument*.

To make a *CLI argument* optional, use `typer.Argument()` and pass a different "default" as the first parameter to `typer.Argument()`, for example `None`:

```Python hl_lines="7"
{!../docs_src/arguments/optional/tutorial002_an.py!}
```

Now we have:

```Python
name: Annotated[Optional[str], typer.Argument()] = None
```

Because we are using `typer.Argument()` **Typer** will know that this is a *CLI argument* (no matter if *required* or *optional*).

/// tip

By using `Optional` your editor will be able to know that the value *could* be `None`, and will be able to warn you if you do something assuming it is a `str` that would break if it was `None`.

///

Check the help:

<div class="termy">

```console
// First check the help
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]

Options:
  --help                Show this message and exit.
```

</div>

/// tip

Notice that `NAME` is still a *CLI argument*, it's shown up there in the "`Usage: main.py` ...".

Also notice that now `[NAME]` has brackets ("`[`" and "`]`") around (before it was just `NAME`) to denote that it's **optional**, not **required**.

///

Now run it and test it:

<div class="termy">

```console
// With no CLI argument
$ python main.py

Hello World!

// With one optional CLI argument
$ python main.py Camila

Hello Camila
```

</div>

/// tip

Notice that "`Camila`" here is an optional *CLI argument*, not a *CLI option*, because we didn't use something like "`--name Camila`", we just passed "`Camila`" directly to the program.

///

## Alternative (old) `typer.Argument()` as the default value

**Typer** also supports another older alternative syntax for declaring *CLI arguments* with additional metadata.

Instead of using `Annotated`, you can use `typer.Argument()` as the default value:

```Python hl_lines="4"
{!> ../docs_src/arguments/optional/tutorial001.py!}
```

/// tip

Prefer to use the `Annotated` version if possible.

///

Before, because `name` didn't have any default value it would be a **required parameter** for the Python function, in Python terms.

When using `typer.Argument()` as the default value **Typer** does the same and makes it a **required** *CLI argument*.

We changed it to:

```Python
name: str = typer.Argument()
```

But now as `typer.Argument()` is the "default value" of the function's parameter, it would mean that "it is no longer required" (in Python terms).

As we no longer have the Python function default value (or its absence) to tell if something is required or not and what is the default value, `typer.Argument()` receives a first parameter `default` that serves the same purpose of defining that default value, or making it required.

Not passing any value to the `default` argument is the same as marking it as required. But you can also explicitly mark it as *required* by passing `...` as the `default` argument, passed to `typer.Argument(default=...)`.

```Python
name: str = typer.Argument(default=...)
```

/// info

If you hadn't seen that `...` before: it is a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" class="external-link" target="_blank">part of Python and is called "Ellipsis"</a>.

///

```Python hl_lines="4"
{!> ../docs_src/arguments/optional/tutorial003.py!}
```

And the same way, you can make it optional by passing a different `default` value, for example `None`:

```Python hl_lines="6"
{!> ../docs_src/arguments/optional/tutorial002.py!}
```

Because the first parameter passed to `typer.Argument(default=None)` (the new "default" value) is `None`, **Typer** knows that this is an **optional** *CLI argument*, if no value is provided when calling it in the command line, it will have that default value of `None`.

The `default` argument is the first one, so it's possible that you see code that passes the value without explicitly using `default=`, like:

```Python
name: str = typer.Argument(...)
```

...or like:

```Python
name: str = typer.Argument(None)
```

...but again, try to use `Annotated` if possible, that way your code in terms of Python will mean the same thing as with **Typer** and you won't have to remember any of these details.
