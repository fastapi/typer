<p align="center">
  <a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" alt="Typer"></a>
</p>
<p align="center">
    <em>Typer, build great CLIs. Easy to code. Based on Python type hints.</em>
</p>
<p align="center">
<a href="https://github.com/tiangolo/typer/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/typer/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/tiangolo/typer/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/typer/workflows/Publish/badge.svg" alt="Publish">
</a>
<a href="https://codecov.io/gh/tiangolo/typer" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/typer?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/typer" target="_blank">
    <img src="https://img.shields.io/pypi/v/typer?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://typer.tiangolo.com" target="_blank">https://typer.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/typer" target="_blank">https://github.com/tiangolo/typer</a>

---

Typer is a library for building <abbr title="command line interface, programs executed from a terminal">CLI</abbr> applications that users will **love using** and developers will **love creating**. Based on Python 3.6+ type hints.

The key features are:

* **Intuitive to write**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
* **Easy to use**: It's easy to use for the final users. Automatic help, and automatic completion for all shells.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
* **Start simple**: The simplest example adds only 2 lines of code to your app: **1 import, 1 function call**.
* **Grow large**: Grow in complexity as much as you want, create arbitrarily complex trees of commands and groups of subcommands, with options and arguments.

## FastAPI of CLIs

<a href="https://fastapi.tiangolo.com" target="_blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" style="width: 20%;"></a>

**Typer** is <a href="https://fastapi.tiangolo.com" class="external-link" target="_blank">FastAPI</a>'s little sibling.

And it's intended to be the FastAPI of CLIs.

## Requirements

Python 3.6+

**Typer** stands on the shoulders of a giant. Its only internal dependency is <a href="https://click.palletsprojects.com/" class="external-link" target="_blank">Click</a>.

## Installation

<div class="termy">

```console
$ pip install typer
---> 100%
Successfully installed typer
```

</div>

## Example

### The absolute minimum

* Create a file `main.py` with:

```Python
import typer


def main(name: str):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    typer.run(main)
```

### Run it

Run your application:

<div class="termy">

```console
// Run your application
$ python main.py

// You get a nice error, you are missing NAME
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument 'NAME'.

// You get a --help for free
$ python main.py --help

Usage: main.py [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// When you create a package you get ✨ auto-completion ✨ for free, installed with --install-completion

// Now pass the NAME argument
$ python main.py Camila

Hello Camila

// It works! 🎉
```

</div>

**Note**: auto-completion works when you create a Python package and run it with `--install-completion` or when you use <a href="https://typer.tiangolo.com/typer-cli/" class="internal-link" target="_blank">Typer CLI</a>.

## Example upgrade

This was the simplest example possible.

Now let's see one a bit more complex.

### An example with two subcommands

Modify the file `main.py`.

Create a `typer.Typer()` app, and create two subcommands with their parameters.

```Python hl_lines="3  6  11  20"
import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
```

And that will:

* Explicitly create a `typer.Typer` app.
    * The previous `typer.run` actually creates one implicitly for you.
* Add two subcommands with `@app.command()`.
* Execute the `app()` itself, as if it was a function (instead of `typer.run`).

### Run the upgraded example

<div class="termy">

```console
// Check the --help
$ python main.py --help

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

Commands:
  goodbye
  hello

// You have 2 subcommands (the 2 functions): goodbye and hello

// Now get the --help for hello

$ python main.py hello --help

Usage: main.py hello [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --help  Show this message and exit.

// And now get the --help for goodbye

$ python main.py goodbye --help

Usage: main.py goodbye [OPTIONS] NAME

Arguments:
  NAME  [required]

Options:
  --formal / --no-formal  [default: False]
  --help                  Show this message and exit.

// Automatic --formal and --no-formal for the bool option 🎉

// And if you use it with the hello command

$ python main.py hello Camila

Hello Camila

// And with the goodbye command

$ python main.py goodbye Camila

Bye Camila!

// And with --formal

$ python main.py goodbye --formal Camila

Goodbye Ms. Camila. Have a good day.
```

</div>

### Recap

In summary, you declare **once** the types of parameters (*CLI arguments* and *CLI options*) as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python 3.6+**.

For example, for an `int`:

```Python
total: int
```

or for a `bool` flag:

```Python
force: bool
```

And similarly for **files**, **paths**, **enums** (choices), etc. And there are tools to create **groups of subcommands**, add metadata, extra **validation**, etc.

**You get**: great editor support, including **completion** and **type checks** everywhere.

**Your users get**: automatic **`--help`**, **auto-completion** in their terminal (Bash, Zsh, Fish, PowerShell) when they install your package or when using <a href="https://typer.tiangolo.com/typer-cli/" class="internal-link" target="_blank">Typer CLI</a>.

For a more complete example including more features, see the <a href="https://typer.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

## Optional Dependencies

Typer uses <a href="https://click.palletsprojects.com/" class="external-link" target="_blank">Click</a> internally. That's the only dependency.

But you can also install extras:

* <a href="https://rich.readthedocs.io/en/stable/index.html" class="external-link" target="_blank">Rich</a>: and Typer will show nicely formatted errors automatically.
* <a href="https://pypi.org/project/colorama/" class="external-link" target="_blank"><code>colorama</code></a>: and Click will automatically use it to make sure your terminal's colors always work correctly, even in Windows.
    * Then you can use any tool you want to output your terminal's colors in all the systems, including the integrated `typer.style()` and `typer.secho()` (provided by Click).
    * Or any other tool, e.g. <a href="https://pypi.org/project/wasabi/" class="external-link" target="_blank"><code>wasabi</code></a>, <a href="https://github.com/erikrose/blessings" class="external-link" target="_blank"><code>blessings</code></a>.
* <a href="https://github.com/sarugaku/shellingham" class="external-link" target="_blank"><code>shellingham</code></a>: and Typer will automatically detect the current shell when installing completion.
    * With `shellingham` you can just use `--install-completion`.
    * Without `shellingham`, you have to pass the name of the shell to install completion for, e.g. `--install-completion bash`.

You can install `typer` with `colorama` and `shellingham` with `pip install typer[all]`.

## Other tools and plug-ins

Click has many plug-ins available that you can use. And there are many tools that help with command line applications that you can use as well, even if they are not related to Typer or Click.

For example:

* <a href="https://github.com/click-contrib/click-spinner" class="external-link" target="_blank"><code>click-spinner</code></a>: to show the user that you are loading data. A Click plug-in.
    * There are several other Click plug-ins at <a href="https://github.com/click-contrib" class="external-link" target="_blank">click-contrib</a> that you can explore.
* <a href="https://pypi.org/project/tabulate/" class="external-link" target="_blank"><code>tabulate</code></a>: to automatically display tabular data nicely. Independent of Click or Typer.
* <a href="https://github.com/tqdm/tqdm" class="external-link" target="_blank"><code>tqdm</code></a>: a fast, extensible progress bar, alternative to Typer's own `typer.progressbar()`.
* etc... you can re-use many of the great available tools for building CLIs.

## License

This project is licensed under the terms of the MIT license.
