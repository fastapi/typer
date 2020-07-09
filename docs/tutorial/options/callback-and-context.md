In some occasions you might want to have some custom logic for a specific *CLI parameter* (for a *CLI option*  or *CLI argument*) that is executed with the value received from the terminal.

In those cases you can use a *CLI parameter* callback function.

## Validate *CLI parameters*

For example, you could do some validation before the rest of the code is executed.

```Python hl_lines="4 5 6 7  10"
{!../docs_src/options/callback/tutorial001.py!}
```

Here you pass a function to `typer.Option()` or `typer.Argument()` with the keyword argument `callback`.

The function receives the value from the command line. It can do anything with it, and then return the value.

In this case, if the `--name` is not `Camila` we raise a `typer.BadParameter()` exception.

The `BadParameter` exception is special, it shows the error with the parameter that generated it.

Check it:

<div class="termy">

```console
$ python main.py --name Camila

Hello Camila

$ python main.py --name Rick

Usage: main.py [OPTIONS]

// We get the error from the callback
Error: Invalid value for '--name': Only Camila is allowed
```

</div>

## Handling completion

There's something to be aware of with callbacks and completion that requires some small special handling.

But first let's just use completion in your shell (Bash, Zsh, Fish, or PowerShell).

After installing completion (for your own Python package or for **Typer CLI**), when you use your CLI program and start adding a *CLI option* with `--` an then hit <kbd>TAB</kbd>, your shell will show you the available *CLI options* (the same for *CLI arguments*, etc).

To check it quickly without creating a new Python package, install [Typer CLI](../../typer-cli.md){.internal-link target=_blank} and use it with the previous script:

<div class="termy">

```console
// Hit the TAB key in your keyboard below where you see the: [TAB]
$ typer ./main.py [TAB][TAB]

// Depending on your terminal/shell you will get some completion like this ✨
run    -- Run the provided Typer app.
utils  -- Extra utility commands for Typer apps.

// Then try with "run" and --help
$ typer ./main.py run --help

// You get a help text with your CLI options as you normally would
Usage: typer run [OPTIONS]

  Run the provided Typer app.

Options:
  --name TEXT  [required]
  --help       Show this message and exit.

// Then try completion with your program
$ typer ./main.py run --[TAB][TAB]

// You get completion for CLI options
--help  -- Show this message and exit.
--name

// And you can run it as if it was with Python directly
$ typer ./main.py run --name Camila

Hello Camila
```

</div>

### How shell completion works

The way it works internally is that the shell/terminal will call your CLI program with some special environment variables (that hold the current *CLI parameters*, etc) and your CLI program will print some special values that the shell will use to present completion. All this is handled for you by **Typer** behind the scenes.

But the main **important point** is that it is all based on values printed by your program that the shell reads.

### Breaking completion in a callback

Let's say that when the callback is running, we want to show a message saying that it's validating the name:

```Python hl_lines="5"
{!../docs_src/options/callback/tutorial002.py!}
```

And because the callback will be called when the shell calls your program asking for completion, that message `"Validating name"` will be printed and it will break completion.

It will look something like:

<div class="termy">

```console
// Run it normally
$ typer ./main.py run --name Camila

// See the extra message "Validating name"
Validating name
Hello Camila

$ typer ./main.py run --[TAB][TAB]

// Some weird broken error message ⛔️
(eval):1: command not found: Validating
rutyper ./main.pyed Typer app.
```

</div>

### Fix completion - using the `Context`

When you create a **Typer** application it uses Click underneath.

And every Click application has a special object called a <a href="https://click.palletsprojects.com/en/7.x/commands/#nested-handling-and-contexts" class="external-link" target="_blank">"Context"</a> that is normally hidden.

But you can access the context by declaring a function parameter of type `typer.Context`.

The "context" has some additional data about the current execution of your program:

```Python hl_lines="4 5 6"
{!../docs_src/options/callback/tutorial003.py!}
```

The `ctx.resilient_parsing` will be `True` when handling completion, so you can just return without printing anything else.

But it will be `False` when calling the program normally. So you can continue the execution of your previous code.

That's all is needed to fix completion 🚀

Check it:

<div class="termy">

```console
$ typer ./main.py run --[TAB][TAB]

// Now it works correctly 🎉
--help  -- Show this message and exit.
--name

// And you can call it normally
$ typer ./main.py run --name Camila

Validating name
Hello Camila
```

</div>

## Using the `CallbackParam` object

The same way you can access the `typer.Context` by declaring a function parameter with its value, you can declare another function parameter with type `typer.CallbackParam` to get the specific Click `Parameter` object.

```Python hl_lines="4  7"
{!../docs_src/options/callback/tutorial004.py!}
```

It's probably not very common, but you could do it if you need it.

For example if you had a callback that could be used by several *CLI parameters*, that way the callback could know which parameter is each time.

Check it:

<div class="termy">

```console
$ python main.py --name Camila

Validating param: name
Hello Camila
```

</div>

## Technical Details

Because you get the relevant data in the callback function based on standard Python type annotations, you get type checks and autocompletion in your editor for free.

And **Typer** will make sure you get the function parameters you want.

You don't have to worry about their names, their order, etc.

As it's based on standard Python types, it "**just works**". ✨

### Click's `Parameter`

The `typer.CallbackParam` is actually just a sub-class of Click's <a href="https://click.palletsprojects.com/en/7.x/api/#click.Parameter" class="external-link" target="_blank">`Parameter`</a>, so you get all the right completion in your editor.

### Callback with type annotations

You can get the `typer.Context` and the `typer.CallbackParam` simply by declaring a function parameter of each type.

The order doesn't matter, the name of the function parameters doesn't matter.

You could also get only the `typer.CallbackParam` and not the `typer.Context`, or vice versa, it will still work.

### `value` function parameter

The `value` function parameter in the callback can also have any name (e.g. `lastname`) and any type, but it should have the same type annotation as in the main function, because that's what it will receive.

It's also possible to not declare its type. It will still work.

And it's possible to not declare the `value` parameter at all, and, for example, only get the `typer.Context`. That will also work.
