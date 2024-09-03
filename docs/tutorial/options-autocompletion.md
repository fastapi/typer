# CLI Option autocompletion

As you have seen, apps built with **Typer** have completion in your shell that works when you create a Python package or using the `typer` command.

It normally completes *CLI options*, *CLI arguments*, and subcommands (that you will learn about later).

But you can also provide auto completion for the **values** of *CLI options* and *CLI arguments*. We will learn about that here.

## Review completion

Before checking how to provide custom completions, let's check again how it works.

After installing completion for your own Python package (or using the `typer` command), when you use your CLI program and start adding a *CLI option* with `--` an then hit <kbd>TAB</kbd>, your shell will show you the available *CLI options* (the same for *CLI arguments*, etc).

To check it quickly without creating a new Python package, use the `typer` command.

Then let's create small example program:

//// tab | Python 3.8+

```Python
{!> ../docs_src/options_autocompletion/tutorial001_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python
{!> ../docs_src/options_autocompletion/tutorial001.py!}
```

////

And let's try it with the `typer` command to get completion:

<div class="termy">

```console
// Hit the TAB key in your keyboard below where you see the: [TAB]
$ typer ./main.py [TAB][TAB]

// Depending on your terminal/shell you will get some completion like this ✨
run    -- Run the provided Typer app.
utils  -- Extra utility commands for Typer apps.

// Then try with "run" and --
$ typer ./main.py run --[TAB][TAB]

// You will get completion for --name, depending on your terminal it will look something like this
--name  -- The name to say hi to.

// And you can run it as if it was with Python directly
$ typer ./main.py run --name Camila

Hello Camila
```

</div>

## Custom completion for values

Right now we get completion for the *CLI option* names, but not for the values.

We can provide completion for the values creating an `autocompletion` function, similar to the `callback` functions from [CLI Option Callback and Context](./options/callback-and-context.md){.internal-link target=_blank}:

//// tab | Python 3.8+

```Python hl_lines="5-6  15"
{!> ../docs_src/options_autocompletion/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="4-5  14"
{!> ../docs_src/options_autocompletion/tutorial002.py!}
```

////

We return a `list` of strings from the `complete_name()` function.

And then we get those values when using completion:

<div class="termy">

```console
$ typer ./main.py run --name [TAB][TAB]

// We get the values returned from the function 🎉
Camila     Carlos     Sebastian
```

</div>

We got the basics working. Now let's improve it.

## Check the incomplete value

Right now, we always return those values, even if users start typing `Sebast` and then hit <kbd>TAB</kbd>, they will also get the completion for `Camila` and `Carlos` (depending on the shell), while we should only get completion for `Sebastian`.

But we can fix that so that it always works correctly.

Modify the `complete_name()` function to receive a parameter of type `str`, it will contain the incomplete value.

Then we can check and return only the values that start with the incomplete value from the command line:

//// tab | Python 3.8+

```Python hl_lines="7-12"
{!> ../docs_src/options_autocompletion/tutorial003_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="6-11"
{!> ../docs_src/options_autocompletion/tutorial003.py!}
```

////

Now let's try it:

<div class="termy">

```console
$ typer ./main.py run --name Ca[TAB][TAB]

// We get the values returned from the function that start with Ca 🎉
Camila     Carlos
```

</div>

Now we are only returning the valid values, that start with `Ca`, we are no longer returning `Sebastian` as a completion option.

/// tip

You have to declare the incomplete value of type `str` and that's what you will receive in the function.

No matter if the actual value will be an `int`, or something else, when doing completion, you will only get a `str` as the incomplete value.

And the same way, you can only return `str`, not `int`, etc.

///

## Add help to completions

Right now we are returning a `list` of `str`.

But some shells (Zsh, Fish, PowerShell) are capable of showing extra help text for completion.

We can provide that extra help text so that those shells can show it.

In the `complete_name()` function, instead of providing one `str` per completion element, we provide a `tuple` with 2 items. The first item is the actual completion string, and the second item is the help text.

So, in the end, we return a `list` of `tuples` of `str`:

//// tab | Python 3.8+

```Python hl_lines="4-8  11-17"
{!> ../docs_src/options_autocompletion/tutorial004_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="3-7  10-16"
{!> ../docs_src/options_autocompletion/tutorial004.py!}
```

////

/// tip

If you want to have help text for each item, make sure each item in the list is a `tuple`. Not a `list`.

Click checks specifically for a `tuple` when extracting the help text.

So in the end, the return will be a `list` (or other iterable) of `tuples` of 2 `str`.

///

/// info

The help text will be visible in Zsh, Fish, and PowerShell.

Bash doesn't support showing the help text, but completion will still work the same.

///

If you have a shell like Zsh, it would look like:

<div class="termy">

```console
$ typer ./main.py run --name [TAB][TAB]

// We get the completion items with their help text 🎉
Camila     -- The reader of books.
Carlos     -- The writer of scripts.
Sebastian  -- The type hints guy.
```

</div>

## Simplify with `yield`

Instead of creating and returning a list with values (`str` or `tuple`), we can use `yield` with each value that we want in the completion.

That way our function will be a <a href="https://docs.python.org/3.8/glossary.html#index-19" class="external-link" target="_blank">generator</a> that **Typer** (actually Click) can iterate:

//// tab | Python 3.8+

```Python hl_lines="11-14"
{!> ../docs_src/options_autocompletion/tutorial005_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="10-13"
{!> ../docs_src/options_autocompletion/tutorial005.py!}
```

////

That simplifies our code a bit and works the same.

/// tip

If all the `yield` part seems complex for you, don't worry, you can just use the version with the `list` above.

In the end, that's just to save us a couple of lines of code.

///

/// info

The function can use `yield`, so it doesn't have to return strictly a `list`, it just has to be <a href="https://docs.python.org/3.8/glossary.html#term-iterable" class="external-link" target="_blank">iterable</a>.

But each of the elements for completion has to be a `str` or a `tuple` (when containing a help text).

///

## Access other *CLI parameters* with the Context

Let's say that now we want to modify the program to be able to "say hi" to multiple people at the same time.

So, we will allow multiple `--name` *CLI options*.

/// tip

You will learn more about *CLI parameters* with multiple values later in the tutorial.

So, for now, take this as a sneak peek 😉.

///

For this we use a `List` of `str`:

//// tab | Python 3.8+

```Python hl_lines="9-14"
{!> ../docs_src/options_autocompletion/tutorial006_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8-11"
{!> ../docs_src/options_autocompletion/tutorial006.py!}
```

////

And then we can use it like:

<div class="termy">

```console
$ typer ./main.py run --name Camila --name Sebastian

Hello Camila
Hello Sebastian
```

</div>

### Getting completion for multiple values

And the same way as before, we want to provide **completion** for those names. But we don't want to provide the **same names** for completion if they were already given in previous parameters.

For that, we will access and use the "Context". When you create a **Typer** application it uses Click underneath. And every Click application has a special object called a <a href="https://click.palletsprojects.com/en/7.x/commands/#nested-handling-and-contexts" class="external-link" target="_blank">"Context"</a> that is normally hidden.

But you can access the context by declaring a function parameter of type `typer.Context`.

And from that context you can get the current values for each parameter.

//// tab | Python 3.8+

```Python hl_lines="13-14  16"
{!> ../docs_src/options_autocompletion/tutorial007_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="12-13  15"
{!> ../docs_src/options_autocompletion/tutorial007.py!}
```

////

We are getting the `names` already provided with `--name` in the command line before this completion was triggered.

If there's no `--name` in the command line, it will be `None`, so we use `or []` to make sure we have a `list` (even if empty) to check its contents later.

Then, when we have a completion candidate, we check if each `name` was already provided with `--name` by checking if it's in that list of `names` with `name not in names`.

And then we `yield` each item that has not been used yet.

Check it:

<div class="termy">

```console
$ typer ./main.py run --name [TAB][TAB]

// The first time we trigger completion, we get all the names
Camila     -- The reader of books.
Carlos     -- The writer of scripts.
Sebastian  -- The type hints guy.

// Add a name and trigger completion again
$ typer ./main.py run --name Sebastian --name Ca[TAB][TAB]

// Now we get completion only for the names we haven't used 🎉
Camila  -- The reader of books.
Carlos  -- The writer of scripts.

// And if we add another of the available names:
$ typer ./main.py run --name Sebastian --name Camila --name [TAB][TAB]

// We get completion for the only available one
Carlos  -- The writer of scripts.
```

</div>

/// tip

It's quite possible that if there's only one option left, your shell will complete it right away instead of showing the option with the help text, to save you more typing.

///

## Getting the raw *CLI parameters*

You can also get the raw *CLI parameters*, just a `list` of `str` with everything passed in the command line before the incomplete value.

For example, something like `["typer", "main.py", "run", "--name"]`.

/// tip

This would be for advanced scenarios, in most use cases you would be better off using the context.

But it's still possible if you need it.

///

As a simple example, let's show it on the screen before completion.

Because completion is based on the output printed by your program (handled internally by **Typer**), during completion we can't just print something else as we normally do.

### Printing to "standard error"

/// tip

If you need a refresher about what is "standard output" and "standard error" check the section in [Printing and Colors: "Standard Output" and "Standard Error"](./printing.md#standard-output-and-standard-error){.internal-link target=_blank}.

///

The completion system only reads from "standard output", so, printing to "standard error" won't break completion. 🚀

You can print to "standard error" with a **Rich** `Console(stderr=True)`.

Using `stderr=True` tells **Rich** that the output should be shown in "standard error".

//// tab | Python 3.8+

```Python hl_lines="13  16-17"
{!> ../docs_src/options_autocompletion/tutorial008_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="12  15-16"
{!> ../docs_src/options_autocompletion/tutorial008.py!}
```

////

/// info

If you can't install and use Rich, you can also use `print(lastname, file=sys.stderr)` or `typer.echo("some text", err=True)` instead.

///

We get all the *CLI parameters* as a raw `list` of `str` by declaring a parameter with type `List[str]`, here it's named `args`.

/// tip

Here we name the list of all the raw *CLI parameters* `args` because that's the convention with Click.

But it doesn't contain only *CLI arguments*, it has everything, including *CLI options* and values, as a raw `list` of `str`.

///

And then we just print it to "standard error".

<div class="termy">

```console
$ typer ./main.py run --name [TAB][TAB]

// First we see the raw CLI parameters
['./main.py', 'run', '--name']

// And then we see the actual completion
Camila     -- The reader of books.
Carlos     -- The writer of scripts.
Sebastian  -- The type hints guy.
```

</div>

/// tip

This is a very simple (and quite useless) example, just so you know how it works and that you can use it.

But it's probably useful only in very advanced use cases.

///

## Getting the Context and the raw *CLI parameters*

Of course, you can declare everything if you need it, the context, the raw *CLI parameters*, and the incomplete `str`:

//// tab | Python 3.8+

```Python hl_lines="16"
{!> ../docs_src/options_autocompletion/tutorial009_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="15"
{!> ../docs_src/options_autocompletion/tutorial009.py!}
```

////

Check it:

<div class="termy">

```console
$ typer ./main.py run --name [TAB][TAB]

// First we see the raw CLI parameters
['./main.py', 'run', '--name']

// And then we see the actual completion
Camila     -- The reader of books.
Carlos     -- The writer of scripts.
Sebastian  -- The type hints guy.

$ typer ./main.py run --name Sebastian --name Ca[TAB][TAB]

// Again, we see the raw CLI parameters
['./main.py', 'run', '--name', 'Sebastian', '--name']

// And then we see the rest of the valid completion items
Camila     -- The reader of books.
Carlos     -- The writer of scripts.
```

</div>

## Types, types everywhere

**Typer** uses the type declarations to detect what it has to provide to your `autocompletion` function.

You can declare function parameters of these types:

* `str`: for the incomplete value.
* `typer.Context`: for the current context.
* `List[str]`: for the raw *CLI parameters*.

It doesn't matter how you name them, in which order, or which ones of the 3 options you declare. It will all "**just work**" ✨
