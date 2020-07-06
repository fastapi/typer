To define a *CLI parameter* that can take a value from a predefined set of values you can use a standard Python <a href="https://docs.python.org/3/library/enum.html" class="external-link" target="_blank">`enum.Enum`</a>:

```Python hl_lines="1  6 7 8 9  12 13"
{!../docs_src/parameter_types/enum/tutorial001.py!}
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
  --install-completion          Install completion for the current shell.
  --show-completion             Show completion for the current shell, to copy it or customize the installation.
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

```Python hl_lines="13"
{!../docs_src/parameter_types/enum/tutorial002.py!}
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
