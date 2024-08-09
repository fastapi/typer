# Printing and Colors

You can use the normal `print()` to show information on the screen:

```Python hl_lines="5"
{!../docs_src/first_steps/tutorial001.py!}
```

It will show the output normally:

<div class="termy">

```console
$ python main.py

Hello World
```

</div>

## Use Rich

You can also display beautiful and more complex information using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a>. It comes by default when you install `typer`.

### Use Rich `print`

For the simplest cases, you can just import `print` from `rich` and use it instead of the standard `print`:

```Python hl_lines="2  15"
{!../docs_src/printing/tutorial001.py!}
```

Just with that, **Rich** will be able to print your data with nice colors and structure:

<div class="termy">

```console
$ python main.py

Here's the data
<b>{</b>
    <font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Rick&apos;</font>,
    <font color="#A6E22E">&apos;age&apos;</font>: <font color="#A1EFE4"><b>42</b></font>,
    <font color="#A6E22E">&apos;items&apos;</font>: <b>[</b>
        <b>{</b><font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Portal Gun&apos;</font><b>}</b>,
        <b>{</b><font color="#A6E22E">&apos;name&apos;</font>: <font color="#A6E22E">&apos;Plumbus&apos;</font><b>}</b>
    <b>]</b>,
    <font color="#A6E22E">&apos;active&apos;</font>: <font color="#A6E22E"><i>True</i></font>,
    <font color="#A6E22E">&apos;affiliation&apos;</font>: <font color="#AE81FF"><i>None</i></font>
<b>}</b>
```

</div>

### Rich Markup

Rich also supports a <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">custom markup syntax</a> to set colors and styles, for example:

```Python hl_lines="6"
{!../docs_src/printing/tutorial002.py!}
```

<div class="termy">

```console
$ python main.py

<font color="#F92672"><b>Alert!</b></font> <font color="#A6E22E">Portal gun</font> shooting! 💥
```

</div>

In this example you can see how to use font styles, colors, and even emojis.

To learn more check out the <a href="https://rich.readthedocs.io/en/stable/markup.html" class="external-link" target="_blank">Rich docs</a>.

### Rich Tables

The way Rich works internally is that it uses a `Console` object to display the information.

When you call Rich's `print`, it automatically creates this object and uses it.

But for advanced use cases, you could create a `Console` yourself.

```Python hl_lines="2-3  5  9-12"
{!../docs_src/printing/tutorial003.py!}
```

In this example, we create a `Console`, and a `Table`. And then we can add some rows to the table, and print it.

If you run it, you will see a nicely formatted table:

<div class="termy">

```console
$ python main.py

┏━━━━━━━┳━━━━━━━━━━━━┓
┃<b> Name  </b>┃<b> Item       </b>┃
┡━━━━━━━╇━━━━━━━━━━━━┩
│ Rick  │ Portal Gun │
│ Morty │ Plumbus    │
└───────┴────────────┘
```

</div>

Rich has many other features, as an example, you can check the docs for:

* <a href="https://rich.readthedocs.io/en/stable/prompt.html" class="external-link" target="_blank">Prompt</a>
* <a href="https://rich.readthedocs.io/en/stable/markdown.html" class="external-link" target="_blank">Markdown</a>
* <a href="https://rich.readthedocs.io/en/stable/panel.html" class="external-link" target="_blank">Panel</a>
* ...and more.

### Typer and Rich

If you are wondering what tool should be used for what, **Typer** is useful for structuring the command line application, with options, arguments, subcommands, data validation, etc.

In general, **Typer** tends to be the entry point to your program, taking the first input from the user.

**Rich** is useful for the parts that need to *display* information. Showing beautiful content on the screen.

The best results for your command line application would be achieved combining both **Typer** and **Rich**.

## "Standard Output" and "Standard Error"

The way printing works underneath is that the **operating system** (Linux, Windows, macOS) treats what we print as if our CLI program was **writing text** to a "**virtual file**" called "**standard output**".

When our code "prints" things it is actually "writing" to this "virtual file" of "standard output".

This might seem strange, but that's how the CLI program and the operating system interact with each other.

And then the operating system **shows on the screen** whatever our CLI program "**wrote**" to that "**virtual file**" called "**standard output**".

### Standard Error

And there's another "**virtual file**" called "**standard error**" that is normally only used for errors.

But we can also "print" to "standard error". And both are shown on the terminal to the users.

/// info

If you use PowerShell it's quite possible that what you print to "standard error" won't be shown in the terminal.

In PowerShell, to see "standard error" you would have to check the variable `$Error`.

But it will work normally in Bash, Zsh, and Fish.

///

### Printing to "standard error"

You can print to "standard error" creating a Rich `Console` with `stderr=True`.

/// tip

`stderr` is short for "standard error".

///

Using `stderr=True` tells **Rich** that the output should be shown in "standard error".

```Python hl_lines="4  8"
{!../docs_src/printing/tutorial004.py!}
```

When you try it in the terminal, it will probably just look the same:

<div class="termy">

```console
$ python main.py

Here is something written to standard error
```

</div>

## "Standard Input"

As a final detail, when you type text in your keyboard to your terminal, the operating system also considers it another "**virtual file**" that you are writing text to.

This virtual file is called "**standard input**".

### What is this for

Right now this probably seems quite useless 🤷‍♂.

But understanding that will come handy in the future, for example for autocompletion and testing.

## Typer Echo

/// warning

In most of the cases, for displaying advanced information, it is recommended to use <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a>.

You can probably skip the rest of this section. 🎉😎

///

**Typer** also has a small utility `typer.echo()` to print information on the screen, it comes directly from Click. But normally you shouldn't need it.

For the simplest cases, you can use the standard Python `print()`.

And for the cases where you want to display data more beautifully, or more advanced content, you should use **Rich** instead.

### Why `typer.echo`

`typer.echo()` (which is actually just `click.echo()`) applies some checks to try and convert binary data to strings, and other similar things.

But in most of the cases you wouldn't need it, as in modern Python strings (`str`) already support and use Unicode, and you would rarely deal with pure `bytes` that you want to print on the screen.

If you have some `bytes` objects, you would probably want to decode them intentionally and directly before trying to print them.

And if you want to print data with colors and other features, you are much better off with the more advanced tools in **Rich**.

/// info

`typer.echo()` comes directly from Click, you can read more about it in <a href="https://click.palletsprojects.com/en/7.x/quickstart/#echoing" class="external-link" target="_blank">Click's docs</a>.

///

### Color

/// note | Technical Details

The way color works in terminals is by using some codes (ANSI escape sequences) as part of the text.

So, a colored text is still just a `str`.

///

/// tip

Again, you are much better off using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> for this. 😎

///

You can create colored strings to output to the terminal with `typer.style()`, that gives you `str`s that you can then pass to `typer.echo()`:

```Python hl_lines="7  9"
{!../docs_src/printing/tutorial005.py!}
```

/// tip

The parameters `fg` and `bg` receive strings with the color names for the "**f**ore**g**round" and "**b**ack**g**round" colors. You could simply pass `fg="green"` and `bg="red"`.

But **Typer** provides them all as variables like `typer.colors.GREEN` just so you can use autocompletion while selecting them.

///

Check it:

<div class="use-termynal" data-termynal>
<span data-ty="input">python main.py</span>
<span data-ty>everything is <span style="color: green; font-weight: bold;">good</span></span>
<span data-ty="input">python main.py --no-good</span>
<span data-ty>everything is <span style="color: white; background-color: red;">bad</span></span>
</div>

You can pass these function arguments to `typer.style()`:

* `fg`: the foreground color.
* `bg`: the background color.
* `bold`: enable or disable bold mode.
* `dim`: enable or disable dim mode. This is badly supported.
* `underline`: enable or disable underline.
* `blink`: enable or disable blinking.
* `reverse`: enable or disable inverse rendering (foreground becomes background and the other way round).
* `reset`: by default a reset-all code is added at the end of the string which means that styles do not carry over.  This can be disabled to compose styles.

/// info

You can read more about it in <a href="https://click.palletsprojects.com/en/7.x/api/#click.style" class="external-link" target="_blank">Click's docs about `style()`</a>

///

### `typer.secho()` - style and print

/// tip

In case you didn't see above, you are much better off using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> for this. 😎

///

There's a shorter form to style and print at the same time with `typer.secho()` it's like `typer.echo()` but also adds style like `typer.style()`:

```Python hl_lines="5"
{!../docs_src/printing/tutorial006.py!}
```

Check it:

<div class="use-termynal" data-termynal>
<span data-ty="input">python main.py Camila</span>
<span style="color: magenta;" data-ty>Welcome here Camila</span>
</div>
