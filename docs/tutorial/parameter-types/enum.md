# Enum - Choices

To define a *CLI parameter* that can take a value from a predefined set of values you can use a standard Python <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">`enum.Enum`</a>:

{* docs_src/parameter_types/enum/tutorial001.py hl[1,6,7,8,9,12,13] *}

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

{* docs_src/parameter_types/enum/tutorial002_an.py hl[15] *}

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

### Using Enum names instead of values

Sometimes you want to accept `Enum` names from the command line and convert
that into `Enum` values in the command handler. You can enable this by setting
`enum_by_name=True`:

{* docs_src/parameter_types/enum/tutorial007_an.py hl[14] *}

And then the names of the `Enum` will be used instead of values:

<div class="termy">

```console
$ python main.py --log-level debug

Log level set to DEBUG
```

</div>

This can be particularly useful if the enum values are not strings:

{* docs_src/parameter_types/enum/tutorial005_an.py hl[8:11,14] *}

```console
$ python main.py --access protected

Access level: protected (2)
```


### List of Enum values

A *CLI parameter* can also take a list of `Enum` values:

{* docs_src/parameter_types/enum/tutorial003_an.py hl[14] *}

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

You can also combine `enum_by_name=True` with a list of enums:

{* docs_src/parameter_types/enum/tutorial006_an.py hl[15] *}

This works exactly the same, but you're using the enum names instead of values:

<div class="termy">

```console
// Try it with a single value
$ python main.py --groceries "f1"

Buying groceries: Eggs

// Try it with multiple values
$ python main.py --groceries "f1" --groceries "f2"

Buying groceries: Eggs, Bacon
```

</div>


### Literal choices

You can also use `Literal` to represent a set of possible predefined choices, without having to use an `Enum`:

{* docs_src/parameter_types/enum/tutorial004_an.py hl[6] *}

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
