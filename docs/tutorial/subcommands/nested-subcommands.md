We'll now see how these same ideas can be extended for deeply nested commands.

Let's imagine that the same *CLI program* from the previous examples now needs to handle `lands`.

But a land could be a `reign` or `town`.

And each of those could have their own commands, like `create` and `delete`.

## A CLI app for reigns

Let's start with a file `reigns.py`:

```Python
{!../docs_src/subcommands/tutorial003/reigns.py!}
```

This is already a simple *CLI program* to manage reigns:

<div class="termy">

```console
// Check the help
$ python reigns.py --help

Usage: reigns.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  conquer
  destroy

// Try it
$ python reigns.py conquer Cintra

Conquering reign: Cintra

$ python reigns.py destroy Mordor

Destroying reign: Mordor
```

</div>

## A CLI app for towns

And now the equivalent for managing towns in `towns.py`:

```Python
{!../docs_src/subcommands/tutorial003/towns.py!}
```

With it, you can manage towns:

<div class="termy">

```console
// Check the help
$ python towns.py --help

Usage: towns.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  burn
  found

// Try it
$ python towns.py found "New Asgard"

Founding town: New Asgard

$ python towns.py burn Vizima

Burning town: Vizima
```

</div>

## Manage the land in a CLI app

Now let's put the `reigns` and `towns` together in the same *CLI program* in `lands.py`:

```Python
{!../docs_src/subcommands/tutorial003/lands.py!}
```

And now we have a single *CLI program* with a command (or command group) `reigns` that has its own commands. And another command `towns` with its own subcommands.

Check it:

<div class="termy">

```console
// Check the help
$ python lands.py --help

Usage: lands.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  reigns
  towns

// We still have the help for reigns
$ python lands.py reigns --help

Usage: lands.py reigns [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  conquer
  destroy

// And the help for towns
$ python lands.py towns --help

Usage: lands.py towns [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  burn
  found
```

</div>

Now try it, manage the lands through the CLI:

<div class="termy">

```console
// Try the reigns command
$ python lands.py reigns conquer Gondor

Conquering reign: Gondor

$ python lands.py reigns destroy Nilfgaard

Destroying reign: Nilfgaard

// Try the towns command
$ python lands.py towns found Springfield

Founding town: Springfield

$ python lands.py towns burn Atlantis

Burning town: Atlantis
```

</div>

## Deeply nested subcommands

Now let's say that all these commands in the `lands.py` *CLI program* should be part of the previous *CLI program* we built in the first example.

We want our *CLI program* to have these commands/command groups:

* `users`:
    * `create`
    * `delete`
* `items`:
    * `create`
    * `delete`
    * `sell`
* `lands`:
    * `reigns`:
        * `conquer`
        * `destroy`
    * `towns`:
        * `found`
        * `burn`

This already is a quite deeply nested "tree" of commands/command groups.

But to achieve that, we just have to add the `lands` **Typer** app to the same `main.py` file we already had:

```Python hl_lines="4  10"
{!../docs_src/subcommands/tutorial003/main.py!}
```

And now we have everything in a single *CLI program*:

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
  items
  lands
  users

// Try some users commands
$ python main.py users create Camila

Creating user: Camila

// Now try some items commands
$ python main.py items create Sword

Creating item: Sword

// And now some lands commands for reigns
$ python main.py lands reigns conquer Gondor

Conquering reign: Gondor

// And for towns
$ python main.py lands towns found Cartagena

Founding town: Cartagena
```

</div>

## Review the files

Here are all the files if you want to review/copy them:

`reigns.py`:

```Python
{!../docs_src/subcommands/tutorial003/reigns.py!}
```

`towns.py`:

```Python
{!../docs_src/subcommands/tutorial003/towns.py!}
```

`lands.py`:

```Python
{!../docs_src/subcommands/tutorial003/lands.py!}
```

`users.py`:

```Python
{!../docs_src/subcommands/tutorial003/users.py!}
```

`items.py`:

```Python
{!../docs_src/subcommands/tutorial003/items.py!}
```

`main.py`:

```Python
{!../docs_src/subcommands/tutorial003/main.py!}
```

!!! tip
    All these files have an `if __name__ == "__main__"` block just to demonstrate how each of them can also be an independent *CLI app*.

    But for your final application, only `main.py` would need it.

## Recap

That's it, you can just add **Typer** applications one inside another as much as you want and create complex *CLI programs* while writing simple code.

You can probably achieve a simpler *CLI program* design that's easier to use than the example here. But if your requirements are complex, **Typer** helps you build your *CLI app* easily.

!!! tip
    Auto completion helps a lot, specially with complex programs.

    Check the docs about adding auto completion to your *CLI apps*.
