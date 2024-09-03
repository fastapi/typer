# CLI Arguments with Multiple Values

*CLI arguments* can also receive multiple values.

You can define the type of a *CLI argument* using `typing.List`.

```Python hl_lines="7"
{!../docs_src/multiple_values/arguments_with_multiple_values/tutorial001.py!}
```

And then you can pass it as many *CLI arguments* of that type as you want:

<div class="termy">

```console
$ python main.py ./index.md ./first-steps.md woohoo!

This file exists: index.md
woohoo!
This file exists: first-steps.md
woohoo!
```

</div>

/// tip

We also declared a final *CLI argument* `celebration`, and it's correctly used even if we pass an arbitrary number of `files` first.

///

/// info

A `List` can only be used in the last command (if there are subcommands), as this will take anything to the right and assume it's part of the expected *CLI arguments*.

///

## *CLI arguments* with tuples

If you want a specific number of values and types, you can use a tuple, and it can even have default values:

//// tab | Python 3.8+

```Python hl_lines="8-10"
{!> ../docs_src/multiple_values/arguments_with_multiple_values/tutorial002_an.py!}
```

////

//// tab | Python 3.8+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7-8"
{!> ../docs_src/multiple_values/arguments_with_multiple_values/tutorial002.py!}
```

////

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

Usage: main.py [OPTIONS] [NAMES]...

Arguments:
  [NAMES]...  Select 3 characters to play with  [default: Harry, Hermione, Ron]

Options:
  --help                Show this message and exit.

// Use it with its defaults
$ python main.py

Hello Harry
Hello Hermione
Hello Ron

// If you pass an invalid number of arguments you will get an error
$ python main.py Draco Hagrid

Error: Argument 'names' takes 3 values

// And if you pass the exact number of values it will work correctly
$ python main.py Draco Hagrid Dobby

Hello Draco
Hello Hagrid
Hello Dobby
```

</div>
