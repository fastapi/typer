We'll start with the core idea.

To add a `typer.Typer()` app inside of another.

## Manage items

Let's imagine that you are creating a *CLI program* to manage items in some distant land.

It could be in an `items.py` file with this:

```Python
{!../docs_src/subcommands/tutorial001/items.py!}
```

And you would use it like:

<div class="termy">

```console
$ python items.py create Wand

Creating item: Wand
```

</div>

## Manage users

But then you realize that you also have to manage users from your *CLI app*.

It could be a file `users.py` with something like:

```Python
{!../docs_src/subcommands/tutorial001/users.py!}
```

And you would use it like:

<div class="termy">

```console
$ python users.py create Camila

Creating user: Camila
```

</div>

## Put them together

Both parts are similar. In fact, `items.py` and `users.py` both have commands `create` and `delete`.

But we need them to be part of the same *CLI program*.

In this case, as with `git remote`, we can put them together as subcommands in another `typer.Typer()` *CLI program*.

Now create a `main.py` with:

```Python hl_lines="3 4  7 8"
{!../docs_src/subcommands/tutorial001/main.py!}
```

Here's what we do in `main.py`:

* Import the other Python modules (the files `users.py` and `items.py`).
* Create the main `typer.Typer()` application.
* Use `app.add_typer()` to include the `app` from `items.py` and `users.py`, each of those 2 was also created with `typer.Typer()`.
* Define a `name` with the command that will be used for each of these "sub-Typers" to group their own commands.

And now your *CLI program* has 2 commands:

* `users`: with all of the commands (subcommands) in the `app` from `users.py`.
* `items` with all the commands (subcommands) in the `app` from `items.py`.

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  items
  users
```

</div>

Now you have a *CLI program* with commands `items` and `users`, and they in turn have their own commands (subcommands).

Let's check the `items` command:

<div class="termy">

```console
// Check the help for items
$ python main.py items --help

// It shows its own commands (subcommands): create, delete, sell
Usage: main.py items [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create
  delete
  sell

// Try it
$ python main.py items create Wand

Creating item: Wand

$ python main.py items sell Vase

Selling item: Vase
```

</div>

!!! tip
    Notice that we are still calling `$ python main.py` but now we are using the command `items`.

And now check the command `users`, with all its subcommands:

<div class="termy">

```console
$ python main.py users --help

Usage: main.py users [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  create
  delete

// Try it
$ python main.py users create Camila

Creating user: Camila
```

</div>

## Recap

That's the core idea.

You can just create `typer.Typer()` apps and add them inside one another.

And you can do that with any levels of commands that you want.

Do you need sub-sub-sub-subcommands? Go ahead, create all the `typer.Typer()`s you need and put them together with `app.add_typer()`.

In the next sections we'll update this with more features, but you already have the core idea.

This way, in the same spirit of Click, **Typer** applications are composable, each `typer.Typer()` can be a *CLI app* by itself, but it can also be added as a command group to another Typer app.
