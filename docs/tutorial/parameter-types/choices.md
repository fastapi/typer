To define a *CLI parameter* that can take a value from a predefined set of values you can use a standard Python
<a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">`enum.Enum`</a> or the
standard type hint <a href="https://docs.python.org/3/library/typing.html#typing.Literal" class="external-link" target="_blank">`typing.Literal`</a>

# Enum

```Python hl_lines="1  6 7 8 9  12 13"
{!../docs_src/parameter_types/choices/tutorial001.py!}
```

!!! tip
    Notice that the function parameter `network` will be an `Enum`, not a `str`.

    To get the `str` value in your function's code use `network.value`.

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

Error: Invalid value for '--network': invalid choice: capsule. (choose from simple, conv, lstm)
```

</div>

### Case insensitive Enum choices

You can make an `Enum` (choice) *CLI parameter* be case-insensitive with the `case_sensitive` parameter:

=== "Python 3.6+"

    ```Python hl_lines="15"
    {!> ../docs_src/parameter_types/choices/tutorial002_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="13"
    {!> ../docs_src/parameter_types/choices/tutorial002.py!}
    ```

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


## Literal

```Python hl_lines="2  4  7"
{!../docs_src/parameter_types/choices/tutorial003.py!}
```

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

Error: Invalid value for '--network': invalid choice: capsule. (choose from simple, conv, lstm)
```

</div>

### Case insensitive Literal choices

You can make an `Literal` (choice) *CLI parameter* be case-insensitive with the `case_sensitive` parameter:

=== "Python 3.6+"

    ```Python hl_lines="8"
    {!> ../docs_src/parameter_types/choices/tutorial004_an.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="7"
    {!> ../docs_src/parameter_types/choices/tutorial004.py!}
    ```

And then the values of the `Literal` will be checked no matter if lower case, upper case, or a mix:

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
