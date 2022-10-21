So far we've been concerned with creating and grouping several sub-commands using the
`add_typer` functionality. But what if we want to add a sub-command to an existing
command?

The motivating example for the subcommand feature that we talked about in the
[introduction of this tutorial](./index.md) was the `git remote` command.
You can simply use `git remote` to list the current remote repositories, but you can
also use `git remote add` to add a new remote repository.
The command and the  sub-command are essentially independent,
but hierarchically grouped.

If you recall the example from the [previous section](./single-file.md), there we
defined  a CLI with two commands, namely `users` and `items`, each with several
sub-commands. If you simply wanted to run `python main.py users` as a "base command",
this simply would not work, because we'd have to specify a sub-command, like `create`.

## Typer apps with commands and sub-commands

Let's see how to create a command line tool with Typer that can handle this situation.
We're going to keep things self-contained and create a Typer app in a single file.
Let's say we create a file called `main.py` in which we store all our Typer code.
We want the Typer CLI to do the following:

- We want a command called `remote` that we can call _without_ any sub-commands.
- On top of that, we also want to define a sub-command to `remote` called `add`
  that has to be called with two mandatory arguments.

Here's how you can create such an app with Typer.
First, we define two apps, namely a main `app` and a `remote` app.
We then use the `callback` decorator on our `app` to enhance its output.
The `add` command is a vanilla Typer command, there's nothing special about it.

What's special is the definition of the `remote` command itself.
To define it, we have to use the so-called _Context_ of the Typer app,
which you can read more on in the [Context tutorial](../commands/context.md).
In essence, the Typer Context allows you to control the flow of your app on a more
granular level, for instance by inspecting if a command was called with a sub-command
or not.

Specifically, we tell Typer to invoke the `remote` command even if no sub-command
is specified by setting `invoke_without_command=True` in the `callback` decorator.
Note that we have to use `callback` here, and not `command`, as you might have
suspected.
Also, in the body of `remote`, we catch the case where no sub-command was specified by
checking if `ctx.invoked_subcommand` is `None`.

```Python hl_lines="12 13 14 15"
{!../docs_src/subcommands/tutorial004/main.py!}
```

## Running the app

Now, we can run the app and see how it works!
First, let's check out the help message of the main app:

<div class="termy">

```console
// Check the main help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  remote  Adding a remote
```

</div>

This clearly tells us that there is one single command in this app, namely `remote`.
Let's run this one, too, and see what happens:

<div class="termy">

```console
$ python main.py remote

This is the remote main command. You can also use the 'add' sub-command.
```

</div>

The `remote` command simply prints a message in this case, but you could make it do
whatever you want.

In any case, next we want to run the `add` sub-command, which takes two arguments.
This command is built to mimic the `git remote add` command as introduced at the
[beginning of this tutorial](./index.md).

<div class="termy">

```console
$ python main.py remote add upstream https://github.com/tiangolo/typer.git

Adding remote upstream with url https://github.com/tiangolo/typer.git
```

</div>

This is all you need to know to build executable commands with subcommands.
This can be useful, especially if you want to extend an existing command with a new
subcommand.

In the next section, you're going to learn how to _nest_ subcommands, which can be
combined with the techniques you learned in this section.
