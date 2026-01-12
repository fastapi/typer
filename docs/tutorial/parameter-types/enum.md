# Enum - Choices

To define a *CLI parameter* that can take a value from a predefined set of values you can use a standard Python <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">`enum.Enum`</a>:

{* docs_src/parameter_types/enum/tutorial001_py39.py hl[1,6:9,16:17] *}

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

{* docs_src/parameter_types/enum/tutorial002_an_py39.py hl[19] *}

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

{* docs_src/parameter_types/enum/tutorial003_an_py39.py hl[17] *}

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

### Literal choices

You can also use `Literal` to represent a set of possible predefined choices, without having to use an `Enum`:

{* docs_src/parameter_types/enum/tutorial004_an_py310.py hl[10] *}

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
```

</div>
