## The simplest example

The simplest Typer file could look like this:

```Python
{!./src/first_steps/tutorial001.py!}
```

Copy that to a file `main.py`.

Test it:

```bash
python main.py
```

You will see an output like:

```hl_lines=""
Hello World
```

It just prints "Hello World".

If you type:

```bash
python main.py --help
```

it shows:

```
Usage: main.py [OPTIONS]

Options:
  --help  Show this message and exit.
```

...but this program is still not very useful. Let's increase that.

## What is a **CLI argument**

Here we will use the word **CLI argument** to refer to **CLI parameters** passed in some specific order to the CLI application. By default, they are *required*.

If you go to your terminal and type:

```bash
ls ./myproject
```

`ls` will show the contents of the directory `./myproject`.

* `ls` is the *command* (or "program", "CLI app").
* `./myproject` is a *CLI argument*.

They are a bit different from **CLI options** that you will see later below.

## Add a CLI argument

Update the previous example with an argument `name`:

```Python hl_lines="4 5"
{!./src/first_steps/tutorial002.py!}
```

If you run it without the argument:

```bash
python main.py
```

it shows:

```
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument "NAME".
```

Now pass that `name` *CLI argument*:

```bash
python main.py Camila
```

it shows:

```
Hello Camila
```

Here `Camila` is the *CLI argument*.

## Two CLI arguments

Now extend that to have 2 arguments, `name` and `lastname`:

```Python hl_lines="4 5"
{!./src/first_steps/tutorial003.py!}
```

Now get the help:

```bash
python main.py --help
```

it shows:

```
Usage: main.py [OPTIONS] NAME LASTNAME

Options:
  --help  Show this message and exit.
```

There are now 2 *CLI arguments*, `name` and `lastname`.

Now pass a single `name` argument:

```bash
python main.py Camila
```

it shows:

```
Usage: main.py [OPTIONS] NAME LASTNAME
Try "main.py --help" for help.

Error: Missing argument "LASTNAME".
```

These 2 arguments are required, so, pass both:

```bash
python main.py Camila Gutiérrez
```

it shows:

```
Hello Camila Gutiérrez
```

!!! tip
    Notice that the order is important. The last name has to go after the first name.

    If you called it with:

    ```bash
    python main.py Gutiérrez Camila
    ```

    your app wouldn't have a way to know which is the `name` and which the `lastname`. It expects the first *CLI argument* to be the `name` and the second *CLI argument* to be the `lastname`.

## What is a **CLI option**

Here we will use the word **CLI option** to refer to **CLI parameters** passed to the CLI application with a specific name. Because they have a name they don't depend on the order. By default they are *optional* (not *required*).

They are a bit different from **CLI arguments** that you already created.

If you go to your terminal and type:

```bash
ls ./myproject --size
```

`ls` will show the contents of the directory `./myproject` with their `size`.

* `ls` is the *command* (or "program", "CLI app").
* `./myproject` is a *CLI argument*.
* `--size` is an optional *CLI option*.

A *CLI option* like `--size` doesn't depend on the order like a *CLI argument*.

The program knows it has to show the size because it sees `--size`, not because of the order.

So, if you put the `--size` *before* the *CLI argument*, it still works:

```bash
ls --size ./myproject
```

!!! tip
    In this example above the *CLI option* `--size` is just a "flag", it's a boolean value, `True` or `False`.

    This one doesn't receive any values. But *CLI options* can also receive values like *CLI arguments*. You'll see how later.

## Add one *CLI option*

Now add a `--formal` *CLI option*:

```Python hl_lines="4 5"
{!./src/first_steps/tutorial004.py!}
```

Here `formal` is a `bool` that is `False` by default.

If you get the help:

```bash
python main.py --help
```

it shows:

```
Usage: main.py [OPTIONS] NAME LASTNAME

Options:
  --formal / --no-formal
  --help                  Show this message and exit.
```

!!! tip
    Notice that it automatically creates a `--formal` and a `--no-formal` because it detected that `formal` is a `bool`.

Now call it normally:

```bash
python main.py Camila Gutiérrez
```

it still shows:

```
Hello Camila Gutiérrez
```

But if you pass `--formal`:

```bash
python main.py Camila Gutiérrez --formal
```

it shows:

```
Good day Ms. Camila Gutiérrez.
```

And as `formal` is a *CLI option*, you can put it anywhere in this command:

```bash
python main.py Camila --formal Gutiérrez
```

and:

```bash
python main.py --formal Camila Gutiérrez
```

both still show:

```
Good day Ms. Camila Gutiérrez.
```

## A **CLI option* with a value

Let's convert the `lastname` from a *CLI argument* to a *CLI option*:

```Python hl_lines="4"
{!./src/first_steps/tutorial005.py!}
```

As `lastname` now has a default value of `""` (an empty string) it is no longer required in the function, and **Typer** will now by default make it an optional *CLI option*.

If you get the help:

```bash
python main.py --help
```

it now shows:

```
Usage: main.py [OPTIONS] NAME

Options:
  --lastname TEXT
  --formal / --no-formal
  --help                  Show this message and exit.
```

!!! tip
    Notice the `--lastname`, and notice that it takes a textual value.

If you call it without a `--lastname`:

```bash
python main.py Camila
```

it shows:

```
Hello Camila
```

and you can pass the `--lastname`:

```bash
python main.py Camila --lastname Gutiérrez
```

and it shows:

```
Hello Camila Gutiérrez
```

And as `--lastname` is now a *CLI option* that doesn't depend on the order, you can pass it before the name:

```bash
python main.py --lastname Gutiérrez Camila
```

and it will still work normally:

```
Hello Camila Gutiérrez
```

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
    
    ```Python
    def bring_person(name: str, lastname: str = ""):
        pass
    ```

    The other refers to the value passed when *calling* a function. Like:

    ```Python
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

When talking about command line interfaces/applications, the words "argument" and "parameter" are commonly used to refer to that data passed to a CLI app, those parameters.

But those words don't imply anything about the data being required, needing to be passed in a certain order, nor having a flag like `--lastname`.

The parameters that come with a flag like `--lastname` and a value (or  when the flag itself is the value, like `--formal`) are commonly optional, not required. So, when talking about CLIs it's common to call them *optional arguments* or *optional parameters*.

In reality, the parameters that require an order can be made *optional* too. And the ones that come with a flag (like `--lastname`) can be *required* too.

### In **Typer**

To try and make it a bit easier, we'll normally use the words "parameter" or "argument" to refer to Python functions.

We'll use ***CLI argument*** to refer to those *CLI parameters* that depend on an order. That are **required** by default.

And we'll use ***CLI option*** to refer to those *CLI parameters* that depend on a flag (like `--lastname`). That are **optional** by default.

We will use ***CLI parameter*** to refer to both, *CLI arguments* and *CLI options*.
