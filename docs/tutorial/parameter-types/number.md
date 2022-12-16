You can define numeric validations with `max` and `min` values for `int` and `float` *CLI parameters*:

```Python hl_lines="5 6 7"
{!../docs_src/parameter_types/number/tutorial001.py!}
```

*CLI arguments* and *CLI options* can both use these validations.

You can specify `min`, `max` or both.

Check it:

<div class="termy">

```console
$ python main.py --help

// Notice the extra RANGE in the help text for --age and --score
Usage: main.py [OPTIONS] ID

Arguments:
  ID  [required]

Options:
  --age INTEGER RANGE   [default: 20]
  --score FLOAT RANGE   [default: 0]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Pass all the CLI parameters
$ python main.py 5 --age 20 --score 90

ID is 5
--age is 20
--score is 90.0

// Pass an invalid ID
$ python main.py 1002

Usage: main.py [OPTIONS] ID
Try "main.py --help" for help.

Error: Invalid value for 'ID': 1002 is not in the valid range of 0 to 1000.

// Pass an invalid age
$ python main.py 5 --age 15

Usage: main.py [OPTIONS] ID
Try "main.py --help" for help.

Error: Invalid value for '--age': 15 is smaller than the minimum valid value 18.

// Pass an invalid score
$ python main.py 5 --age 20 --score 100.5

Usage: main.py [OPTIONS] ID
Try "main.py --help" for help.

Error: Invalid value for '--score': 100.5 is bigger than the maximum valid value 100.

// But as we didn't specify a minimum score, this is accepted
$ python main.py 5 --age 20 --score -5

ID is 5
--age is 20
--score is -5.0
```

</div>

## Clamping numbers

You might want to, instead of showing an error, use the closest minimum or maximum valid values.

You can do it with the `clamp` parameter:

```Python hl_lines="5 6 7"
{!../docs_src/parameter_types/number/tutorial002.py!}
```

And then, when you pass data that is out of the valid range, it will be "clamped", the closest valid value will be used:

<div class="termy">

```console
// ID doesn't have clamp, so it shows an error
$ python main.py 1002

Usage: main.py [OPTIONS] ID
Try "main.py --help" for help.

Error: Invalid value for 'ID': 1002 is not in the valid range of 0 to 1000.

// But --rank and --score use clamp
$ python main.py 5 --rank 11 --score -5

ID is 5
--rank is 10
--score is 0
```

</div>

## Counter *CLI options*

You can make a *CLI option* work as a counter with the `counter` parameter:

```Python hl_lines="4"
{!../docs_src/parameter_types/number/tutorial003.py!}
```

It means that the *CLI option* will be like a boolean flag, e.g. `--verbose`.

And the value you receive in the function will be the amount of times that `--verbose` was added:

<div class="termy">

```console
// Check it
$ python main.py

Verbose level is 0

// Now use one --verbose
$ python main.py --verbose

Verbose level is 1

// Now 3 --verbose
$ python main.py --verbose --verbose --verbose

Verbose level is 3

// And with the short name
$ python main.py -v

Verbose level is 1

// And with the short name 3 times
$ python main.py -v -v -v

Verbose level is 3

// As short names can be put together, this also works
$ python main.py -vvv

Verbose level is 3
```

</div>
