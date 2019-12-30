We have seen how to create a CLI program with possibly several *CLI Options* and *CLI Arguments*.

But **Typer** allows you to create CLI programs with several commands (also known as subcommands).

For example, the program `git` has several commands.

One command of `git` is `git push`. And `git push` in turn takes its own *CLI arguments* and *CLI options*.

For example:

<div class="termy">

```console
// The push command with no parameters
$ git push

---> 100%

// The push command with one CLI option --set-upstream and 2 CLI arguments
$ git push --set-upstream origin master

---> 100%
```

</div>

Another command of `git` is `git pull`, it also has some *CLI parameters*.

It's like if the same big program `git` had several small programs inside.

!!! tip
    A command looks the same as a *CLI argument*, it's just some name without a preceding `--`. But commands have predefined name, and are used to group different sets of functionalities into the same CLI application.

## Command or subcommand

It's common to call a CLI program a "command".

But when one of these programs have subcommands, those subcommands are also frequently called just "commands".

Have that in mind so you don't get confused.

Here I'll use **CLI application** or **program** to refer to the program you are building in Python with Typer, and **command** to refer to one of these "subcommands" of your program.

## Explicit application

Before creating CLI applications with multiple commands/subcommands we need to understand how to create an explicit `typer.Typer()` application.

In the *CLI Options* and *CLI Argument* tutorials you have seen how to create a single function and then pass that function to `typer.run()`.

For example:

```Python hl_lines="9"
{!./src/first_steps/tutorial002.py!}
```

But that is actually a shortcut. Under the hood, **Typer** converts that to a CLI application with `typer.Typer()` and executes it. All that inside of `typer.run()`.

There's also a more explicit way to achieve the same:

```Python hl_lines="3  6  12"
{!./src/commands/tutorial001.py!}
```

When you use `typer.run()`, **Typer** is doing more or less the same as above, it will:

* Create a new `typer.Typer()` "application".
* Create a new "`command`" with your function.
* Call the same "application" as if it was a function with "`app()`".

!!! info "`@decorator` Info"
    That `@something` syntax in Python is called a "decorator".

    You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).

    A "decorator" takes the function below and does something with it.

    In our case, this decorator tells **Typer** that the function below is a "`command`".

Both ways, with `typer.run()` and creating the explicit application, achieve the same.

!!! tip
    If your use case is solved with just `typer.run()`, that's fine, you don't have to create the explicit `app` and use `@app.command()`, etc.

    You might want to do that later when your app needs the extra features, but if it doesn't need them yet, that's fine.

If you run the second example, with the explicit `app`, it works exactly the same:

<div class="termy">

```console
// Without a CLI argument
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument "NAME".

// With the NAME CLI argument
$ python main.py Camila

Hello Camila

// Asking for help
$ python main.py  --help

Usage: main.py [OPTIONS] NAME

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

## A CLI application with multiple commands

Coming back to the CLI applications with multiple commands/subcommands, **Typer** allows creating CLI applications with multiple of them.

Now that you know how to create an explicit `typer.Typer()` application and add one command, let's see how to add multiple commands.

Let's say that we have a CLI application to manage users.

We'll have a command to `create` users and another command to `delete` them.

To begin, let's say it can only create and delete one single predefined user:

```Python hl_lines="6  11"
{!./src/commands/tutorial002.py!}
```

Now we have a CLI application with 2 commands, `create` and `delete`:

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
  create
  delete

// Test them
$ python main.py create

Creating user: Hiro Hamada

$ python main.py delete

Deleting user: Hiro Hamada

// Now we have 2 commands! 🎉
```

</div>

Notice that the help text now shows the 2 commands: `create` and `delete`.

!!! tip
    By default, the names of the commands are generated from the function name.

## Command *CLI arguments*

The same way as with a CLI application with a single command, subcommands (or just "commands") can also have their own *CLI arguments*:

```Python hl_lines="7  12"
{!./src/commands/tutorial003.py!}
```

<div class="termy">

```console
// Check the help for create
$ python main.py create --help

Usage: main.py create [OPTIONS] USERNAME

Options:
  --help  Show this message and exit.

// Call it with a CLI argument
$ python main.py create Camila

Creating user: Camila

// The same for delete
$ python main.py delete Camila

Deleting user: Camila
```

</div>

!!! tip
    Everything to the *right* of the *command* are *CLI parameters* (*CLI arguments* and *CLI options*) for that command.

!!! note "Technical Details"
    Actually, it's everything to the right of that command, *before any subcommand*.

    It's possible to have groups of *subcommands*, it's like if one *command* also had *subcommands*. And then those *subcommands* could have their own *CLI parameters*, taking their own *CLI parameters*.

    You will see about them later in another section.

## Command *CLI options*

Commands can also have their own *CLI options*.

In fact, each command can have different *CLI arguments* and *CLI options*:

```Python hl_lines="7  13 14  24  33"
{!./src/commands/tutorial004.py!}
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

## Command help

The same as before, you can add help for the commands in the docstrings and the *CLI options*.

And the `typer.Typer()` application receives a parameter `help` that you can pass with the main help text for your CLI program:

```Python hl_lines="3  8 9 10  20  23 24 25 26 27  39  42 43 44 45 46  55 56 57"
{!./src/commands/tutorial005.py!}
```

Check it:

<div class="termy">

```console
// Check the new help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Awesome CLI user manager.

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  create      Create a new user with USERNAME.
  delete      Delete a user with USERNAME.
  delete-all  Delete ALL users in the database.
  init        Initialize the users database.

// Now the commands have inline help 🎉

// Check the help for create
$ python main.py create --help

Usage: main.py create [OPTIONS] USERNAME

  Create a new user with USERNAME.

Options:
  --help  Show this message and exit.

// Check the help for delete
$ python main.py delete --help

Usage: main.py delete [OPTIONS] USERNAME

  Delete a user with USERNAME.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for delete-all
$ python main.py delete-all --help

Usage: main.py delete-all [OPTIONS]

  Delete ALL users in the database.

  If --force is not used, will ask for confirmation.

Options:
  --force / --no-force  Force deletion without confirmation.  [required]
  --help                Show this message and exit.

// Check the help for init
$ python main.py init --help

Usage: main.py init [OPTIONS]

  Initialize the users database.

Options:
  --help  Show this message and exit.
```

</div>

!!! tip
    `typer.Typer()` receives several other parameters for other things, we'll see that later.

    You will also see how to use "Callbacks" later, and those include a way to add this same help message in a function docstring.

## Custom command name

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

```Python hl_lines="6  11"
{!./src/commands/tutorial006.py!}
```

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

## One command vs multiple commands

You might have noticed that if you create a single command, as in the first example:

```Python hl_lines="3  6  12"
{!./src/commands/tutorial001.py!}
```

**Typer** is smart enough to create a CLI application with that single function as the main CLI application, not as a command/subcommand:

<div class="termy">

```console
// Without a CLI argument
$ python main.py

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument "NAME".

// With the NAME CLI argument
$ python main.py Camila

Hello Camila

// Asking for help
$ python main.py

Usage: main.py [OPTIONS] NAME

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

!!! tip
    Notice that it doesn't show a command `main`, even though the function name is `main`.

But if you add multiple commands, **Typer** will create one *CLI command* for each one of them:

```Python hl_lines="6  11"
{!./src/commands/tutorial002.py!}
```

Here we have 2 commands `create` and `delete`:

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
  create
  delete

// Test the commands
$ python main.py create

Creating user: Hiro Hamada

$ python main.py delete

Deleting user: Hiro Hamada
```

</div>

!!! tip
    This is **Typer**'s behavior by default, but you could still create a CLI application with one single command, like:

    ```
    $ python main.py main
    ```

    instead of just:

    ```
    $ python main.py
    ```

    You will learn more about this in the section about application Callbacks.

## Decorator Technical Details

When you use `@app.command()` the function under the decorator is registered in the **Typer** application and is then used later by the application.

But Typer doesn't modify that function itself, the function is left as is.

That means that if your function is simple enough that you could create it without using `typer.Option()` or `typer.Argument()`, you could use the same function for a **Typer** application and a **FastAPI** application putting both decorators on top, or similar tricks.

!!! note "Click Technical Details"
    This behavior is a design difference with Click.

    In Click, when you add a `@click.command()` decorator it actually modifies the function underneath and replaces it with an object.
