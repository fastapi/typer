## *CLI options* with help

In the *First Steps* section you saw how to add help for a CLI app/command by adding it to a function's <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr>.

Here's how that last example looked like:

```Python
{!./src/first_steps/tutorial006.py!}
```

Now we'll add a *help* section to the *CLI options*:

```Python hl_lines="6 7"
{!./src/options/tutorial001.py!}
```

We are replacing the default values we had before with `typer.Option()`.

As we no longer have a default value there, the first parameter to `typer.Option()` serves the same purpose of defining that default value.

So, if we had:

```Python
lastname: str = ""
```

now we write:

```Python
lastname: str = typer.Option("")
```

And both forms achieve the same: a *CLI option* with a default value of an empty string (`""`).

And then we can pass the `help` keyword parameter:

```Python
lastname: str = typer.Option("", help="this option does this and that")
```

to create the help for that *CLI option*.

Copy that example from above to a file `main.py`.

Test it:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] NAME

  Say hi to NAME, optionally with a --lastname.

  If --formal is used, say hi very formally.

Options:
  --lastname TEXT         Last name of person to greet.
  --formal / --no-formal  Say hi formally.
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.

// Now you have a help text for the --lastname and --formal CLI options 🎉
```

</div>

## Make a *CLI option* required

We said before that *by default*:

* *CLI options* are **optional**
* *CLI arguments* are **required**

Well, that's how they work *by default*, and that's the convention in many CLI programs and systems.

But if you really want, you can change that.

To make a *CLI option* required, pass `...` to `typer.Option()`.

!!! info
    If you hadn't seen that `...` before: it is a a special single value, it is <a href="https://docs.python.org/3/library/constants.html#Ellipsis" target="_blank">part of Python and is called "Ellipsis"</a>.

That will tell **Typer** that it's still a *CLI option*, but it doesn't have a default value, and it's required.

Let's make the `--lastname` a required *CLI option*.

We'll also simplify the example to focus on the new parts:

```Python hl_lines="4"
{!./src/options/tutorial002.py!}
```

!!! tip
    You could still add `help` to `typer.Option()` as before, but we are omitting it here to simplify the example.

And test it:

<div class="termy">

```console
// Pass the NAME CLI argument
$ python main.py Camila

// We didn't pass the now required --lastname CLI option
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing option "--lastname".

// Now update it to pass the required --lastname CLI option
$ python main.py Camila --lastname Gutiérrez

Hello Camila Gutiérrez

// And if you check the help
$ python main.py --help

Usage: main.py [OPTIONS] NAME

Options:
  --lastname TEXT       [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// It now tells you that --lastname is required 🎉
```

</div>

## Prompt for a *CLI option*

It's also possible to, instead of just showing an error, ask for the missing value with `prompt=True`:

```Python hl_lines="4"
{!./src/options/tutorial003.py!}
```

And then your program will ask the user for it in the terminal:

<div class="termy">

```console
// Call it with the NAME CLI argument
$ python main.py Camila

// It asks for the missing CLI option --lastname
# Lastname: $ Gutiérrez

Hello Camila Gutiérrez
```

</div>

### Customize the prompt

You can also set a custom prompt, passing the string that you want to use instead of just `True`:

```Python hl_lines="6"
{!./src/options/tutorial004.py!}
```

And then your program will ask for it using with your custom prompt:

<div class="termy">

```console
// Call it with the NAME CLI argument
$ python main.py Camila

// It uses the custom prompt
# Please tell me your last name: $ Gutiérrez

Hello Camila Gutiérrez
```

</div>

## Confirmation prompt

In some cases you could want to prompt for something and then ask the user to confirm it by typing it twice.

You can do it passing the parameter `confirmation_prompt=True`.

Let's say it's a CLI app to delete a project:

```Python hl_lines="4"
{!./src/options/tutorial005.py!}
```

And it will prompt the user for a value and then for the confirmation:

<div class="termy">

```console
$ python main.py

// Your app will first prompt for the project name, and then for the confirmation
# Project name: $ Old Project
# Repeat for confirmation: $ Old Project

Deleting project Old Project

// If the user doesn't type the same, receives an error and a new prompt
$ python main.py

# Project name: $ Old Project
# Repeat for confirmation: $ New Spice

Error: the two entered values do not match

# Project name: $ Old Project
# Repeat for confirmation: $ Old Project

Deleting project Old Project

// Now it works 🎉
```

</div>

## Show default in help

You can tell Typer to show the default value in the help text with `show_default=True`:

```Python hl_lines="4"
{!./src/options/tutorial006.py!}
```

And it will show up in the help text:

<div class="termy">

```console
$ python main.py

Hello Wade Wilson

// Show the help
$ python main.py --help

Usage: main.py [OPTIONS]

Options:
  --fullname TEXT       [default: Wade Wilson]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

!!! tip
    Notice the `[default: Wade Wilson]` in the help text.

## Other uses

`typer.Option()` has several other users. For data validation, to enable other features, etc.

But you will see about that later in the docs.
