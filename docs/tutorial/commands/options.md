Commands can also have their own *CLI options*.

In fact, each command can have different *CLI arguments* and *CLI options*:

```Python hl_lines="7  13 14  24  33"
{!../docs_src/commands/options/tutorial001.py!}
```

Here we have multiple commands, with different *CLI parameters*:

* `create`:
    * `username`: a *CLI argument*.
* `delete`:
    * `username`: a *CLI argument*.
    * `--force`: a *CLI option*, if not provided, it's prompted.
* `delete-all`:
    * `--force`: a *CLI option*, if not provided, it's prompted.
* `init`:
    * Doesn't take any *CLI parameters*.

<div class="termy">

```console
// Check the help
python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  create
  delete
  delete-all
  info
```

</div>

!!! tip
    Check the command `delete-all`, by default command names are generated from the function name, replacing `_` with `-`.

Test it:

<div class="termy">

```console
// Check the command create
$ python main.py create Camila

Creating user: Camila

// Now test the command delete
$ python main.py delete Camila

# Are you sure you want to delete the user? [y/N]: $ y

Deleting user: Camila

$ python main.py delete Wade

# Are you sure you want to delete the user? [y/N]: $ n

Operation cancelled

// And finally, the command delete-all
// Notice it doesn't have CLI arguments, only a CLI option

$ python main.py delete-all

# Are you sure you want to delete ALL users? [y/N]: $ y

Deleting all users

$ python main.py delete-all

# Are you sure you want to delete ALL users? [y/N]: $ n

Operation cancelled

// And if you pass the --force CLI option, it doesn't need to confirm

$ python main.py delete-all --force

Deleting all users

// And init that doesn't take any CLI parameter
$ python main.py init

Initializing user database
```

</div>
