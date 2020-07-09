We have seen how to create a CLI program with possibly several *CLI options* and *CLI arguments*.

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
    A command looks the same as a *CLI argument*, it's just some name without a preceding `--`. But commands have a predefined name, and are used to group different sets of functionalities into the same CLI application.

## Command or subcommand

It's common to call a CLI program a "command".

But when one of these programs have subcommands, those subcommands are also frequently called just "commands".

Have that in mind so you don't get confused.

Here I'll use **CLI application** or **program** to refer to the program you are building in Python with Typer, and **command** to refer to one of these "subcommands" of your program.

## Explicit application

Before creating CLI applications with multiple commands/subcommands we need to understand how to create an explicit `typer.Typer()` application.

In the *CLI options* and *CLI argument* tutorials you have seen how to create a single function and then pass that function to `typer.run()`.

For example:

```Python hl_lines="9"
{!../docs_src/first_steps/tutorial002.py!}
```

But that is actually a shortcut. Under the hood, **Typer** converts that to a CLI application with `typer.Typer()` and executes it. All that inside of `typer.run()`.

There's also a more explicit way to achieve the same:

```Python hl_lines="3  6  12"
{!../docs_src/commands/index/tutorial001.py!}
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

Error: Missing argument 'NAME'.

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
{!../docs_src/commands/index/tutorial002.py!}
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

## Click Group

If you come from Click, a `typer.Typer` app with subcommands is more or less the equivalent of a <a href="https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands" class="external-link" target="_blank">Click Group</a>.

!!! note "Technical Details"
    A `typer.Typer` app is *not* a Click Group, but it provides the equivalent functionality. And it creates a Click Group when calling it.

    It is not directly a Group because **Typer** doesn't modify the functions in your code to convert them to another type of object, it only registers them.

## Decorator Technical Details

When you use `@app.command()` the function under the decorator is registered in the **Typer** application and is then used later by the application.

But Typer doesn't modify that function itself, the function is left as is.

That means that if your function is simple enough that you could create it without using `typer.Option()` or `typer.Argument()`, you could use the same function for a **Typer** application and a **FastAPI** application putting both decorators on top, or similar tricks.

!!! note "Click Technical Details"
    This behavior is a design difference with Click.

    In Click, when you add a `@click.command()` decorator it actually modifies the function underneath and replaces it with an object.
