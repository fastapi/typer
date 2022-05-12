## The simplest example

The simplest **Typer** file could look like this:

```Python
{!../docs_src/first_steps/tutorial001.py!}
```

!!! tip
    You will learn more about `typer.echo()` later in the docs.

Copy that to a file `main.py`.

Test it:

<div class="termy">

```console
$ python main.py

Hello World

// It just prints "Hello World".

// Now check the --help
$ python main.py --help

Usage: main.py [OPTIONS]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.
```

</div>

...but this program is still not very useful. Let's extend it.

## What is a **CLI argument**

Here we will use the word **CLI argument** to refer to **CLI parameters** passed in some specific order to the CLI application. By default, they are *required*.

If you go to your terminal and type:

<div class="termy">

```bash
$ ls ./myproject

first-steps.md  intro.md
```

</div>

`ls` will show the contents of the directory `./myproject`.

* `ls` is the *program* (or "command", "CLI app").
* `./myproject` is a *CLI argument*, in this case it refers to the path of a directory.

They are a bit different from **CLI options** that you will see later below.

## Add a CLI argument

Update the previous example with an argument `name`:

```Python hl_lines="4 5"
{!../docs_src/first_steps/tutorial002.py!}
```

<div class="termy">

```console

$ python main.py

// If you run it without the argument, it shows a nice error
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.

// Now pass that NAME CLI argument
$ python main.py Camila

Hello Camila

// Here "Camila" is the CLI argument

// To pass a name with spaces for the same CLI argument, use quotes
$ python main.py "Camila Gutiérrez"

Hello Camila Gutiérrez
```

</div>

!!! tip
    If you need to pass a single value that contains spaces to a *CLI argument*, use quotes (`"`) around it.

## Two CLI arguments

Now let's say we want to have the name and last name separated.

So, extend that to have 2 arguments, `name` and `lastname`:

```Python hl_lines="4 5"
{!../docs_src/first_steps/tutorial003.py!}
```

<div class="termy">

```console
// Check the main --help
$ python main.py --help

Usage: main.py [OPTIONS] NAME LASTNAME

Arguments:
  NAME      [required]
  LASTNAME  [required]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// There are now 2 CLI arguments, name and lastname

// Now pass a single name argument
$ python main.py Camila

Usage: main.py [OPTIONS] NAME LASTNAME
Try "main.py --help" for help.

Error: Missing argument 'LASTNAME'.

// These 2 arguments are required, so, pass both:
$ python main.py Camila Gutiérrez

Hello Camila Gutiérrez
```

</div>

!!! tip
    Notice that the order is important. The last name has to go after the first name.

    If you called it with:

    ```
    $ python main.py Gutiérrez Camila
    ```

    your app wouldn't have a way to know which is the `name` and which the `lastname`. It expects the first *CLI argument* to be the `name` and the second *CLI argument* to be the `lastname`.

## What is a **CLI option**

Here we will use the word **CLI option** to refer to *CLI parameters* passed to the CLI application with a specific name. For example, if you go to your terminal and type:

<div class="termy">

```console
$ ls ./myproject --size

12 first-steps.md   4 intro.md
```

</div>

`ls` will show the contents of the directory `./myproject` with their `size`.

* `ls` is the *program* (or "command", "CLI app").
* `./myproject` is a *CLI argument*.
* `--size` is an optional *CLI option*.

The program knows it has to show the size because it sees `--size`, not because of the order.

A *CLI option* like `--size` doesn't depend on the order like a *CLI argument*.

So, if you put the `--size` *before* the *CLI argument*, it still works (in fact, that's the most common way of doing it):

<div class="termy">

```console
$ ls --size ./myproject

12 first-steps.md   4 intro.md
```

</div>

The main visual difference between a *CLI option* and a *CLI argument* is that the *CLI option* has `--` prepended to the name, like in "`--size`".

A *CLI option* doesn't depend on the order because it has a predefined name (here it's `--size`). This is because the CLI app is looking specifically for a literal `--size` parameter (also known as "flag" or "switch"), with that specific "name" (here the specific name is "`--size`"). The CLI app will check if you typed it or not, it will be actively looking for `--size` even if you didn't type it (to check if it's there or not).

In contrast, the CLI app is not actively looking for the *CLI argument* with a text "`./myproject`", it has no way to know if you would type `./myproject` or `./my-super-awesome-project` or anything else. It's just waiting to get whatever you give it. The only way to know that you refer to a specific *CLI argument* is because of the order. The same way that it knows that the first *CLI argument* was the `name` and the second was the `lastname`, but if you mixed the order, it wouldn't be able to handle it.

Instead, with a *CLI option*, the order doesn't matter.

Also, by default, a *CLI option* is *optional* (not *required*).

So, by default:

* A *CLI argument* is **required**
* A *CLI option* is **optional**

But the *required* and *optional* defaults can be changed.

So, the main and **most important** difference is that:

* *CLI options* **start with `--`** and don't depend on the order
* *CLI arguments* depend on the **sequence order**

!!! tip
    In this example above the *CLI option* `--size` is just a "flag" or "switch" that will contain a boolean value, `True` or `False`, depending on if it was added to the command or not.

    This one doesn't receive any values. But *CLI options* can also receive values like *CLI arguments*. You'll see how later.

## Add one *CLI option*

Now add a `--formal` *CLI option*:

```Python hl_lines="4 5"
{!../docs_src/first_steps/tutorial004.py!}
```

Here `formal` is a `bool` that is `False` by default.

<div class="termy">

```console
// Get the help
$ python main.py --help

Usage: main.py [OPTIONS] NAME LASTNAME

Arguments:
  NAME      [required]
  LASTNAME  [required]

Options:
  --formal / --no-formal  [default: False]
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.
```

</div>

!!! tip
    Notice that it automatically creates a `--formal` and a `--no-formal` because it detected that `formal` is a `bool`.

Now call it normally:

<div class="termy">

```console
$ python main.py Camila Gutiérrez

Hello Camila Gutiérrez

// But if you pass --formal
$ python main.py Camila Gutiérrez --formal

Good day Ms. Camila Gutiérrez.

// And as --formal is a CLI option you can put it anywhere in this command
$ python main.py Camila --formal Gutiérrez

Good day Ms. Camila Gutiérrez.

$ python main.py --formal Camila Gutiérrez

Good day Ms. Camila Gutiérrez.
```

</div>

## A *CLI option* with a value

To convert the `lastname` from a *CLI argument* to a *CLI option*, give it a default value of `""`:

```Python hl_lines="4"
{!../docs_src/first_steps/tutorial005.py!}
```

As `lastname` now has a default value of `""` (an empty string) it is no longer required in the function, and **Typer** will now by default make it an optional *CLI option*.

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --lastname TEXT         [default: ]
  --formal / --no-formal  [default: False]
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.
```

</div>

!!! tip
    Notice the `--lastname`, and notice that it takes a textual value.

    A *CLI option* with a value like `--lastname` (contrary to a *CLI option* without a value, a `bool` flag, like `--formal` or `--size`) takes as its value whatever is at the *right side* of the *CLI option*.

<div class="termy">

```console
// Call it without a --lastname
$ python main.py Camila

Hello Camila

// Pass the --lastname
$ python main.py Camila --lastname Gutiérrez

Hello Camila Gutiérrez
```

</div>

!!! tip
    Notice that "`Gutiérrez`" is at the right side of `--lastname`. A *CLI option* with a value takes as its value whatever is at the *right side*.

And as `--lastname` is now a *CLI option* that doesn't depend on the order, you can pass it before the name:

<div class="termy">

```console
$ python main.py --lastname Gutiérrez Camila

// and it will still work normally
Hello Camila Gutiérrez
```

</div>

## Document your CLI app

If you add a <abbr title="a multi-line string as the first expression inside a function (not assigned to any variable) used for documentation">docstring</abbr> to your function it will be used in the help text:

```Python hl_lines="5 6 7 8 9"
{!../docs_src/first_steps/tutorial006.py!}
```

Now see it with the `--help` option:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] NAME

  Say hi to NAME, optionally with a --lastname.

  If --formal is used, say hi very formally.

Arguments:
  NAME  [required]

Options:
  --lastname TEXT         [default: ]
  --formal / --no-formal  [default: False]
  --install-completion    Install completion for the current shell.
  --show-completion       Show completion for the current shell, to copy it or customize the installation.
  --help                  Show this message and exit.
```

</div>

!!! tip
    There is another place to document the specific *CLI options* and *CLI arguments* that will show up next to them in the help text as with `--install-completion` or `--help`, you will learn that later in the tutorial.

## Arguments, options, parameters, optional, required

Be aware that these terms refer to multiple things depending on the context, and sadly, those "contexts" mix frequently, so it's easy to get confused.

### In Python

In Python, the names of the variables in a function, like `name` and `lastname`:

```Python
def main(name: str, lastname: str = ""):
    pass
```

are called "Python function parameters" or "Python function arguments".

!!! note "Technical Details"
    There's actually a very small distinction in Python between "parameter" and "argument".

    It's quite technical... and somewhat pedantic.

    One refers to the variable name in a function *declaration*. Like:

    ```
    def bring_person(name: str, lastname: str = ""):
        pass
    ```

    The other refers to the value passed when *calling* a function. Like:

    ```
    person = bring_person("Camila", lastname="Gutiérrez")
    ```

    ...but you will probably see them used interchangeably in most of the places (including here).

#### Python default values

In Python, in a function, a parameter with a *default value* like `lastname` in:

```Python
def main(name: str, lastname: str = ""):
    pass
```

is considered an "optional parameter" (or "optional argument").

The default value can be anything, like `""` or `None`.

And a parameter like `name`, that doesn't have a default value, is considered *required*.

### In CLIs

When talking about command line interface applications, the words **"argument"** and **"parameter"** are commonly used to refer to that data passed to a CLI app, those parameters.

But those words **don't imply** anything about the data being required, needing to be passed in a certain order, nor having a flag like `--lastname`.

The parameters that come with a name like `--lastname` (and optionally a value) are commonly optional, not required. So, when talking about CLIs it's common to call them **optional arguments** or **optional parameters**. Sometimes these *optional parameters* that start with `--` are also called a **flag** or a **switch**.

In reality, the parameters that require an order can be made *optional* too. And the ones that come with a flag (like `--lastname`) can be *required* too.

### In **Typer**

To try and make it a bit easier, we'll normally use the words "parameter" or "argument" to refer to Python functions.

We'll use ***CLI argument*** to refer to those *CLI parameters* that depend on the specific order. That are **required** by default.

And we'll use ***CLI option*** to refer to those *CLI parameters* that depend on a name that starts with `--` (like `--lastname`). That are **optional** by default.

We will use ***CLI parameter*** to refer to both, *CLI arguments* and *CLI options*.

## **Typer CLI**

Now that you know the basics of **Typer**, you might want to install and use [Typer CLI](../typer-cli.md){.internal-link target=_blank}.

**Typer CLI** is a tool to run your **Typer** scripts giving you ✨ auto completion ✨ in your terminal.

As an alternative to running with Python:

<div class="termy">

```console
$ python main.py

Hello World
```

</div>

You can run with **Typer CLI**:

<div class="termy">

```console
$ typer main.py run

Hello World
```

</div>

...and it will give you auto completion in your terminal when you hit <kbd>TAB</kbd> for all your code.

So you can use it to have auto completion for your own scripts as you continue with the tutorial.

!!! tip
    Your CLI application built with **Typer** won't need [Typer CLI](../typer-cli.md){.internal-link target=_blank} to have auto completion once you create a Python package.

    But for short scripts and for learning, before creating a Python package, it might be useful.
