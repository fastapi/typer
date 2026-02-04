# Custom Command Name

By default, the command names are generated from the function name.

So, if your function is something like:

```Python
def create(username: str):
    ...
```

Then the command name will be `create`.

But if you already had a function called `create()` somewhere in your code, you would have to name your CLI function differently.

And what if you wanted the command to still be named `create`?

For this, you can set the name of the command in the first parameter for the `@app.command()` decorator:

{* docs_src/commands/name/tutorial001_py39.py hl[6,11] *}

Now, even though the functions are named `cli_create_user()` and `cli_delete_user()`, the commands will still be named `create` and `delete`:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  create
  delete

// Test it
$ python main.py create Camila

Creating user: Camila
```

</div>

Note that any underscores in the function name will be replaced with dashes.

So if your function is something like:

```Python
def create_user(username: str):
    ...
```
Then the command name will be `create-user`.

## Command Aliases

You can define aliases for commands so users can call them with different names.

### Positional Aliases

Pass additional positional arguments to `@app.command()`:

{* docs_src/commands/name/tutorial002_py39.py hl[6,9] *}

The `list` command can be called with `list` or `ls`:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  list, ls
  remove, rm, delete

$ python main.py list

Listing items

$ python main.py ls

Listing items

$ python main.py remove

Removing items

$ python main.py rm

Removing items

$ python main.py delete

Removing items
```

</div>

### Keyword Aliases

Use the `aliases` parameter:

{* docs_src/commands/name/tutorial002_py39.py hl[9] *}

Positional aliases and the `aliases` parameter can be combined.

### Hidden Aliases

Use `hidden_aliases` for aliases that work but don't appear in help:

{* docs_src/commands/name/tutorial003_py39.py hl[6] *}

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  list, ls
  remove

$ python main.py secretlist

Listing items
```

</div>
