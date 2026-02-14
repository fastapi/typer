# CLI Arguments with Environment Variables

You can also configure a *CLI argument* to read a value from an environment variable if it is not provided in the command line as a *CLI argument*.

/// tip

You can learn more about environment variables in the [Environment Variables](../../environment-variables.md){.internal-link target=_blank} page.

///

To do that, use the `envvar` parameter for `typer.Argument()`:

{* docs_src/arguments/envvar/tutorial001_an_py39.py hl[9] *}

In this case, the *CLI argument* `name` will have a default value of `"World"`, but will also read any value passed to the environment variable `AWESOME_NAME` if no value is provided in the command line:

<div class="termy">

```console
// Check the help
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [env var: AWESOME_NAME;default: World]

Options:
  --help                Show this message and exit.

// Call it without a CLI argument
$ python main.py

Hello Mr. World

// Now pass a value for the CLI argument
$ python main.py Czernobog

Hello Mr. Czernobog

// And now use the environment variable
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday

// CLI arguments take precedence over env vars
$ AWESOME_NAME=Wednesday python main.py Czernobog

Hello Mr. Czernobog
```

</div>

## Multiple environment variables

You are not restricted to a single environment variable, you can declare a list of environment variables that could be used to get a value if it was not passed in the command line:

{* docs_src/arguments/envvar/tutorial002_an_py39.py hl[10] *}

Check it:

<div class="termy">

```console
// Check the help
$ python main.py --help

Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [env var: AWESOME_NAME, GOD_NAME;default: World]

Options:
  --help                Show this message and exit.

// Try the first env var
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday

// Try the second env var
$ GOD_NAME=Anubis python main.py

Hello Mr. Anubis
```

</div>

## Hide an env var from the help text

By default, environment variables used will be shown in the help text, but you can disable them with `show_envvar=False`:

{* docs_src/arguments/envvar/tutorial003_an_py39.py hl[11] *}

Check it:

<div class="termy">

```console
//Check the help
$ python main.py --help

// It won't show the env var
Usage: main.py [OPTIONS] [NAME]

Arguments:
  [NAME]  [default: World]

Options:
  --help                Show this message and exit.

// But it will still be able to use it
$ AWESOME_NAME=Wednesday python main.py

Hello Mr. Wednesday
```

</div>
