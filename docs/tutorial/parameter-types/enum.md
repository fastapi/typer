# Enum - Choices

To define a *CLI parameter* that can take a value from a predefined set of values you can use a standard Python <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">`enum.Enum`</a>:

```Python hl_lines="1  6 7 8 9  12 13"
{!../docs_src/parameter_types/enum/tutorial001.py!}
```

/// tip

Notice that the function parameter `network` will be an `Enum`, not a `str`.

To get the `str` value in your function's code use `network.value`.

///

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice the predefined values [simple|conv|lstm]
Usage: main.py [OPTIONS]

Options:
  --network [simple|conv|lstm]  [default: simple]
  --help                        Show this message and exit.

// Try it
$ python main.py --network conv

Training neural network of type: conv

// Invalid value
$ python main.py --network capsule

Usage: main.py [OPTIONS]
Try "main.py --help" for help.

Error: Invalid value for '--network': 'capsule' is not one of 'simple', 'conv', 'lstm'.

// Note that enums are case sensitive by default
$ python main.py --network CONV

Usage: main.py [OPTIONS]
Try "main.py --help" for help.

Error: Invalid value for '--network': 'CONV' is not one of 'simple', 'conv', 'lstm'.
```

</div>

### Case insensitive Enum choices

You can make an `Enum` (choice) *CLI parameter* be case-insensitive with the `case_sensitive` parameter:

//// tab | Python 3.7+

```Python hl_lines="15"
{!> ../docs_src/parameter_types/enum/tutorial002_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="13"
{!> ../docs_src/parameter_types/enum/tutorial002.py!}
```

////

And then the values of the `Enum` will be checked no matter if lower case, upper case, or a mix:

<div class="termy">

```console
// Notice the upper case CONV
$ python main.py --network CONV

Training neural network of type: conv

// A mix also works
$ python main.py --network LsTm

Training neural network of type: lstm
```

</div>

### List of Enum values

A *CLI parameter* can also take a list of `Enum` values:

//// tab | Python 3.7+

```Python hl_lines="14"
{!> ../docs_src/parameter_types/enum/tutorial003_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="13"
{!> ../docs_src/parameter_types/enum/tutorial003.py!}
```

////

This works just like any other parameter value taking a list of things:

<div class="termy">

```console
$ python main.py --help

// Notice the default values being shown
Usage: main.py [OPTIONS]

Options:
  --groceries [Eggs|Bacon|Cheese]  [default: Eggs, Cheese]
  --help                           Show this message and exit.

// Try it with the default values
$ python main.py

Buying groceries: Eggs, Cheese

// Try it with a single value
$ python main.py --groceries "Eggs"

Buying groceries: Eggs

// Try it with multiple values
$ python main.py --groceries "Eggs" --groceries "Bacon"

Buying groceries: Eggs, Bacon
```

</div>


### Functional API

In order to use an `Enum` created using the <a href="https://docs.python.org/3/library/enum.html#functional-api" class="external-link" target="_blank">functional API</a>, you need to create an enum with string values.

You also need to supply the default value as a string (not the enum):

=== "Python 3.7+"

    ```Python hl_lines="6 10"
    {!> ../docs_src/parameter_types/enum/tutorial004_an.py!}
    ```

=== "Python 3.7+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="5 8"
    {!> ../docs_src/parameter_types/enum/tutorial004.py!}
    ```

Alternatively, you can create an `Enum` that extends both `str` and `Enum`. In Python 3.11+, there is <a href="https://docs.python.org/3.11/library/enum.html#enum.StrEnum" class="external-link" target="_blank">`enum.StrEnum`</a>. For Python 3.10 or earlier, there is the <a href="https://github.com/irgeek/StrEnum" class="external-link" target="_blank">StrEnum package</a>.
