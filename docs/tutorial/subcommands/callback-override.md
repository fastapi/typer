# Sub-Typer Callback Override

When creating a **Typer** app you can define a callback function, it always executes and defines the *CLI arguments* and *CLI options* that go before a command.

When adding a Typer app inside of another, the sub-Typer can also have its own callback.

It can handle any *CLI parameters* that go before its own commands and execute any extra code:

```Python hl_lines="9 10 11"
{!../docs_src/subcommands/callback_override/tutorial001.py!}
```

In this case it doesn't define any *CLI parameters*, it just writes a message.

Check it:

<div class="termy">

```console
$ python main.py users create Camila

// Notice the first message is not created by the command function but by the callback
Running a users command
Creating user: Camila
```

</div>

## Add a callback on creation

It's also possible to add a callback when creating the `typer.Typer()` app that will be added to another Typer app:

```Python hl_lines="6 7  10"
{!../docs_src/subcommands/callback_override/tutorial002.py!}
```

This achieves exactly the same as above, it's just another place to add the callback.

Check it:

<div class="termy">

```console
$ python main.py users create Camila

Running a users command
Creating user: Camila
```

</div>

## Overriding the callback on creation

If a callback was added when creating the `typer.Typer()` app, it's possible to override it with a new one using `@app.callback()`.

This is the same information you saw on the section about [Commands - Typer Callback](../commands/callback.md){.internal-link target=_blank}, and it applies the same for sub-Typer apps:

```Python hl_lines="6 7  10  14 15 16"
{!../docs_src/subcommands/callback_override/tutorial003.py!}
```

Here we had defined a callback when creating the `typer.Typer()` sub-app, but then we override it with a new callback with the function `user_callback()`.

As `@app.callback()` takes precedence over `typer.Typer(callback=some_function)`, now our CLI app will use this new callback.

Check it:

<div class="termy">

```console
$ python main.py users create Camila

// Notice the message from the new callback
Callback override, running users command
Creating user: Camila
```

</div>

## Overriding the callback when adding a sub-Typer

Lastly, you can override the callback defined anywhere else when adding a sub-Typer with `app.add_typer()` using the `callback` parameter.

This has the highest priority:

```Python hl_lines="13 14  17"
{!../docs_src/subcommands/callback_override/tutorial004.py!}
```

Notice that the precedence goes to `app.add_typer()` and is not affected by the order of execution. There's another callback defined below, but the one from `app.add_typer()` wins.

Now when you use the CLI program it will use the new callback function `callback_for_add_typer()`.

Check it:

<div class="termy">

```console
$ python users create Camila

// Notice the message from the callback added in add_typer()
I have the high land! Running users command
Creating user: Camila
```

</div>
