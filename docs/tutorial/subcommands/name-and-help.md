When adding a Typer app to another we have seen how to set the `name` to use for the command.

For example to set the command to `users`:

```Python
app.add_typer(users.app, name="users")
```

## Add a help text

We can also set the `help` while adding a Typer:

```Python hl_lines="6"
{!../docs_src/subcommands/name_help/tutorial001.py!}
```

And then we get that help text for that command in the *CLI program*:

<div class="termy">

```console
// Check the main help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  users  Manage users in the app.

// Check the help for the users command
$ python main.py users --help

Usage: main.py users [OPTIONS] COMMAND [ARGS]...

  Manage users in the app.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

We can set the `name` and `help` in several places, each one taking precedence over the other, overriding the previous value.

Let's see those locations.

!!! tip
    There are other attributes that can be set in that same way in the same places we'll see next.

    But those are documented later in another section.

## Inferring name and help from callback

### Inferring a command's name and help

When you create a command with `@app.command()`, by default, it generates the name from the function name.

And by default, the help text is extracted from the function's docstring.

For example:

```Python
@app.command()
def create(item: str):
    """
    Create an item.
    """
    typer.echo(f"Creating item: {item}")
```

...will create a command `create` with a help text of `Create an item`.

### Inferring name and help from `@app.callback()`

The same way, if you define a callback in a `typer.Typer()`, the help text is extracted from the callback function's docstring.

And if that Typer app is added to another Typer app, the default name of the command is generated from the name of the callback function.

Here's an example:

```Python hl_lines="6  9 10 11 12 13"
{!../docs_src/subcommands/name_help/tutorial002.py!}
```

Notice that now we added the sub-Typer without specifying a `name` nor a `help`.

They are now inferred from the callback function.

The command name will be the same callback function's name: `users`.

And the help text for that `users` command will be the callback function's docstring: `Manage users in the app.`.

Check it:

<div class="termy">

```console
// Check the main help
$ python main.py --help

// Notice the command name "users" and the help text "Manage users in the app."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  users  Manage users in the app.

// Check the help for the users command
$ python main.py users --help

// Notice the main description: "Manage users in the app."
Usage: main.py users [OPTIONS] COMMAND [ARGS]...

  Manage users in the app.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Name and help from callback parameter in `typer.Typer()`

If you pass a `callback` parameter while creating a `typer.Typer(callback=some_function)` it will be used to infer the name and help text.

This has the lowest priority, we'll see later what has a higher priority and can override it.

Check the code:

```Python hl_lines="6 7 8 9  12"
{!../docs_src/subcommands/name_help/tutorial003.py!}
```

This achieves exactly the same as the previous example.

Check it:

<div class="termy">

```console
// Check the main help
$ python main.py --help

// Notice the command name "users" and the help text "Manage users in the app."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  users  Manage users in the app.

// Check the help for the users command
$ python main.py users --help

// Notice the main description: "Manage users in the app."
Usage: main.py users [OPTIONS] COMMAND [ARGS]...

  Manage users in the app.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Override a callback set in `typer.Typer()` with `@app.callback()`

The same as with normal **Typer** apps, if you pass a `callback` to `typer.Typer(callback=some_function)` and then override it with `@app.callback()`, the name and help text will be inferred from the new callback:

```Python hl_lines="16 17 18 19 20"
{!../docs_src/subcommands/name_help/tutorial004.py!}
```

Now the name of the command will be `users` instead of `old-callback`, and the help text will be `Manage users in the app.` instead of `Old callback help.`.

Check it:

<div class="termy">

```console
// Check the main help
$ python main.py --help

// Notice the command name "users" and the help text "Manage users in the app."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  users  Manage users in the app.

// Check the help for the users command
$ python main.py users --help

// Notice the main description: "Manage users in the app."
Usage: main.py users [OPTIONS] COMMAND [ARGS]...

  Manage users in the app.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Infer name and help from callback in `app.add_typer()`

If you override the callback in `app.add_typer()` when including a sub-app, the name and help will be inferred from this callback function.

This takes precedence over inferring the name and help from a callback set in `@sub_app.callback()` and `typer.Typer(callback=sub_app_callback)`.

Check the code:

```Python hl_lines="15 16 17 18  21"
{!../docs_src/subcommands/name_help/tutorial005.py!}
```

Now the command will be `new-users` instead of `users`. And the help text will be `I have the highland! Create some users.` instead of the previous ones.

Check it:

<div class="termy">

```console
// Check the main help
$ python main.py --help

// Check the command new-users and its help text
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  new-users  I have the highland! Create some users.

// Now check the help for the new-users command
$ python main.py new-users --help

// Notice the help text
Usage: main.py new-users [OPTIONS] COMMAND [ARGS]...

  I have the highland! Create some users.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Enough inferring

So, when inferring a name and help text, the precedence order from lowest priority to highest is:

* `sub_app = typer.Typer(callback=some_function)`
* `@sub_app.callback()`
* `app.add_typer(sub_app, callback=new_function)`

That's for inferring the name and help text from functions.

But if you set the name and help text explicitly, that has a higher priority than these.

## Set the name and help

Let's now see the places where you can set the command name and help text, from lowest priority to highest.

!!! tip
    Setting the name and help text explicitly always has a higher precedence than inferring from a callback function.

### Name and help in `typer.Typer()`

You could have all the callbacks and overrides we defined before, but the name and help text was inferred from the function name and docstring.

If you set it explicitly, that takes precedence over inferring.

You can set it when creating a new `typer.Typer()`:

```Python hl_lines="12"
{!../docs_src/subcommands/name_help/tutorial006.py!}
```

!!! info
    The rest of the callbacks and overrides are there only to show you that they don't affect the name and help text when you set it explicitly.

We set an explicit name `exp-users`, and an explicit help `Explicit help.`.

So that will take precedence now.

Check it:

<div class="termy">

```console
// Check the main help
$ python main.py --help

// Notice the command name is exp-users and the help text is "Explicit help."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  exp-users  Explicit help.

// Check the help for the exp-users command
$ python main.py exp-users --help

// Notice the main help text
Usage: main.py exp-users [OPTIONS] COMMAND [ARGS]...

  Explicit help.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Name and help in `@app.callback()`

Any parameter that you use when creating a `typer.Typer()` app can be overridden in the parameters of `@app.callback()`.

Continuing with the previous example, we now override the values in `@user_app.callback()`:

```Python hl_lines="24"
{!../docs_src/subcommands/name_help/tutorial007.py!}
```

And now the command name will be `call-users` and the help text will be `Help from callback for users.`.

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// The command name now is call-users and the help text is "Help from callback for users.".
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  call-users  Help from callback for users.

// Check the call-users command help
$ python main.py call-users --help

// Notice the main help text
Usage: main.py call-users [OPTIONS] COMMAND [ARGS]...

  Help from callback for users.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

### Name and help in `app.add_typer()`

And finally, with the highest priority, you can override all that by explicitly setting the `name` and `help` in `app.add_typer()`, just like we did on the first example above:

```Python hl_lines="21"
{!../docs_src/subcommands/name_help/tutorial008.py!}
```

And now, with the highest priorities of them all, the command name will now be `cake-sith-users` and the help text will be `Unlimited powder! Eh, users.`.

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

// Notice the command name cake-sith-users and the new help text "Unlimited powder! Eh, users."
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  cake-sith-users  Unlimited powder! Eh, users.

// And check the help for the command cake-sith-users
$ python main.py cake-sith-users --help

// Notice the main help text
Usage: main.py cake-sith-users [OPTIONS] COMMAND [ARGS]...

  Unlimited powder! Eh, users.

Options:
  --help  Show this message and exit.

Commands:
  create
```

</div>

## Recap

The precedence to generate a command's name and help, from lowest priority to highest, is:

* Implicitly inferred from `sub_app = typer.Typer(callback=some_function)`
* Implicitly inferred from the callback function under `@sub_app.callback()`
* Implicitly inferred from `app.add_typer(sub_app, callback=some_function)`
* Explicitly set on `sub_app = typer.Typer(name="some-name", help="Some help.")`
* Explicitly set on `@sub_app.callback("some-name", help="Some help.")`
* Explicitly set on `app.add_typer(sub_app, name="some-name", help="Some help.")`

So, `app.add_typer(sub_app, name="some-name", help="Some help.")` always wins.
