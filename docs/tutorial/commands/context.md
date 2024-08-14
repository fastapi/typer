# Using the Context

When you create a **Typer** application it uses Click underneath. And every Click application has a special object called a <a href="https://click.palletsprojects.com/en/8.1.x/commands/#nested-handling-and-contexts" class="external-link" target="_blank">"Context"</a> that is normally hidden.

But you can access the context by declaring a function parameter of type `typer.Context`.

You might have read it in [CLI Option Callback and Context](../options/callback-and-context.md){.internal-link target=_blank}.

The same way, in commands or in the main `Typer` callback you can access the context by declaring a function parameter of type `typer.Context`.

## Getting the context

For example, let's say that you want to execute some logic in a `Typer` callback depending on the subcommand that is being called.

You can get the name of the subcommand from the context:

```Python hl_lines="17  21"
{!../docs_src/commands/context/tutorial001.py!}
```

Check it:

<div class="termy">

```console
$ python main.py create Camila

// We get the message from the callback
About to execute command: create
Creating user: Camila

$ python main.py delete Camila

// We get the message from the callback, this time with delete
About to execute command: delete
Deleting user: Camila
```

</div>

## Executable callback

By default, the callback is only executed right before executing a command.

And if no command is provided, the help message is shown.

But we could make it run even without a subcommand with `invoke_without_command=True`:

```Python hl_lines="16"
{!../docs_src/commands/context/tutorial002.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

// The callback is executed, we don't get the default help message
Initializing database

// Try with a command
$ python main.py create Camila

// The callback is still executed
Initializing database
Creating user: Camila
```

</div>

## Exclusive executable callback

We might not want the callback to be executed if there's already other command that will be executed.

For that, we can get the `typer.Context` and check if there's an invoked command in `ctx.invoked_subcommand`.

If it's `None`, it means that we are not calling a subcommand but the main program (the callback) directly:

```Python hl_lines="17  21"
{!../docs_src/commands/context/tutorial003.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

// The callback is executed
Initializing database

// Check it with a subcommand
$ python main.py create Camila

// This time the callback is not executed
Creating user: Camila
```

</div>

## Configuring the context

You can pass configurations for the context when creating a command or callback.

To read more about the available configurations check the docs for <a href="https://click.palletsprojects.com/en/7.x/api/#context" class="external-link" target="_blank">Click's `Context`</a>.

For example, you could keep additional *CLI parameters* not declared in your CLI program with `ignore_unknown_options` and `allow_extra_args`.

Then you can access those extra raw *CLI parameters* as a `list` of `str` in `ctx.args`:

```Python hl_lines="7  9 10"
{!../docs_src/commands/context/tutorial004.py!}
```

<div class="termy">

```console
$ python main.py --name Camila --city Berlin

Got extra arg: --name
Got extra arg: Camila
Got extra arg: --city
Got extra arg: Berlin
```

</div>

/// tip

Notice that it saves all the extra *CLI parameters* as a raw `list` of `str`, including the *CLI option* names and values, everything together.

///
