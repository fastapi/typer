# CLI Parameter Types

You can use several data types for the *CLI options* and *CLI arguments*, and you can add data validation requirements too.

## Data conversion

When you declare a *CLI parameter* with some type **Typer** will convert the data received in the command line to that data type.

For example:

```Python hl_lines="4"
{!../docs_src/parameter_types/index/tutorial001.py!}
```

In this example, the value received for the *CLI argument* `NAME` will be treated as `str`.

The value for the *CLI option* `--age` will be converted to an `int` and `--height-meters` will be converted to a `float`.

And as `female` is a `bool` *CLI option*, **Typer** will convert it to a "flag" `--female` and the counterpart `--no-female`.

And here's how it looks like:

<div class="termy">

```console
$ python main.py --help

// Notice how --age is an INTEGER and --height-meters is a FLOAT
Usage: main.py [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --age INTEGER           [default: 20]
  --height-meters FLOAT   [default: 1.89]
  --female / --no-female  [default: True]
  --help                  Show this message and exit.

// Call it with CLI parameters
$ python main.py Camila --age 15 --height-meters 1.70 --female

// All the data has the correct Python type
NAME is Camila, of type: class 'str'
--age is 15, of type: class 'int'
--height-meters is 1.7, of type: class 'float'
--female is True, of type: class 'bool'

// And if you pass an incorrect type
$ python main.py Camila --age 15.3

Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Invalid value for '--age': '15.3' is not a valid integer

// Because 15.3 is not an INTEGER (it's a float)
```

</div>

## Watch next

See more about specific types and validations in the next sections...


/// info | Technical Details

All the types you will see in the next sections are handled underneath by <a href="https://click.palletsprojects.com/en/7.x/parameters/#parameter-types" class="external-link" target="_blank">Click's Parameter Types</a>.

///
