You can use `typer.echo()` to print to the screen:

```Python hl_lines="5"
{!./src/first_steps/tutorial001.py!}
```

The reason to use `typer.echo()` instead of just `print()` is that it applies some error corrections in case the terminal is misconfigured, and it will properly output color if it's supported.

!!! info
    `typer.echo()` comes directly from Click, you can read more about it in <a href="https://click.palletsprojects.com/en/7.x/quickstart/#echoing" class="external-link" target="_blank">Click's docs</a>.

Check it:

<div class="termy">

```console
$ python main.py

Hello World
```

</div>

## Color

!!! info
    For colors to work correctly on Windows you need to also install <a href="https://pypi.org/project/colorama/" class="external-link" target="_blank">`colorama`</a>.

    You don't need to call `colorama.init()`. Typer (actually Click) will handle it underneath.

!!! note "Technical Details"
    The way color works in terminals is by using some codes (ASCII codes) as part of the text.

    So, a colored text is still just a `str`.

You can create colored strings to output to the terminal with `typer.style()`, that gives you `str`s that you can then pass to `typer.echo()`:

```Python hl_lines="7  9"
{!./src/printing/tutorial001.py!}
```

!!! tip
    The parameters `fg` and `bg` receive strings with the color names. You could simply pass `fg="green"` and `bg="red"`.

    But **Typer** provides them all as variables like `typer.colors.GREEN` just so you can use autocompletion while selecting them.

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

!!! info
    You can read more about it in <a href="https://click.palletsprojects.com/en/7.x/api/#click.style" class="external-link" target="_blank">Click's docs about `style()`</a>

## `typer.secho()` - style and print

There's a shorter form to style and print at the same time with `typer.secho()` it's like `typer.echo()` but also adds style like `typer.style()`:

```Python hl_lines="5"
{!./src/printing/tutorial002.py!}
```

Check it:

<div class="use-termynal" data-termynal>
<span data-ty="input">python main.py Camila</span>
<span style="color: magenta;" data-ty>Welcome here Camila</span>
</div>
