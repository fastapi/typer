You can specify a custom type for your *CLI parameter* using Click's `ParamType` class.

Instructions for how to build a custom type are described [here](https://click.palletsprojects.com/en/7.x/parameters/#implementing-custom-types) in Click's documentation.

Using a custom *CLI parameter* type overrides **Typer**'s default behavior of converting user inputs based on the function's type annotation.

Custom types are supported for both `typer.Option` and `typer.Argument`.

## Example

```Python hl_lines="33"
{!../docs_src/parameter_types/custom/tutorial001.py!}
```

The above app converts a user input into a Python `dict` before the function `main()` is run.

<div class="termy">

```console
$ python main.py --help
Usage: main.py [OPTIONS]

Options:
  --data JSON           [required]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

// The custom ParamType's converter is run when parsing the data.
$ python main.py --data='{"what_i_like":"Python"}'

You like Python? Me too!
```

</div>
