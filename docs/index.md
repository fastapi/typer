<p align="center">
  <a href="https://typer.tiangolo.com"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" alt="Typer"></a>
</p>
<p align="center">
    <em>Typer: CLIs with autocompletion. While developing and using.</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/typer" target="_blank">
    <img src="https://travis-ci.com/tiangolo/typer.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/typer" target="_blank">
    <img src="https://codecov.io/gh/tiangolo/typer/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/typer" target="_blank">
    <img src="https://badge.fury.io/py/typer.svg" alt="Package version">
</a>
</p>

---

**Documentation**: <a href="https://typer.tiangolo.com" target="_blank">https://typer.tiangolo.com</a>

**Source Code**: <a href="https://github.com/tiangolo/typer" target="_blank">https://github.com/tiangolo/typer</a>

---

Typer is library to build <abbr title="command line interface, programs executed from a terminal">CLI</abbr> applications that users love using and developers love creating. Based on Python 3.6+ type hints.

**Typer** is the little sibling of <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a>. And it's intended to be the FastAPI of CLIs.

The key features are:

* **Intuitive to write**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging. Designed to be easy to use and learn. Less time reading docs.
* **Easy to use**: It's easy to use for the final users. Automatic help commands, and (optional) automatic completion for all shells.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
* **Start simple**: The simplest example adds only 2 lines of code to your app: **1 import, 1 function call**.
* **Grow large**: Grow in complexity as much as you want create arbitrarily complex trees of commands and groups sub-commands, with options and arguments.

## Requirements

Python 3.6+

Typer stands on the shoulders of a giant. Internally it uses <a href="https://click.palletsprojects.com/" target="_blank">Click</a>, that's the only dependency.

## Installation

```bash
pip install typer
```

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

```bash
python main.py
```

you will get a response like:

```
Usage: main.py [OPTIONS] NAME
Try "main.py --help" for help.

Error: Missing argument "NAME".
```

Now pass the `NAME` *argument*:

```bash
python main.py Camila
```

You will get a response like:

```
Hello Camila
```

And you automatically get a `--help` command:

```bash
python main.py --help
```

shows:

```
Usage: main.py [OPTIONS] NAME

Options:
  --help  Show this message and exit.
```

## Example upgrade

The previous example was the extreme in terms of simplicity.

Now let's see one a bit more complex.

### An example with two sub-commands

Modify the file `main.py`.

Create a `typer.Typer()` app, and create two sub-commands with their parameters.

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
* Add two sub-commands with `@app.command()`.
* Execute the `app()` itself, as if it was a function (instead of `typer.run`).

### Run the upgraded example

Get the main `--help`:

```bash
python main.py --help
```

shows:

```
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  goodbye
  hello
```

You have 2 sub-commands (the 2 functions), `goodbye` and `hello`.

Now get the help for `hello`:

```bash
python main.py hello --help
```

shows:

```
Usage: main.py hello [OPTIONS] NAME

Options:
  --help  Show this message and exit.
```

And now get the help for `goodbye`:

```bash
python main.py goodbye --help
```

shows:

```
Usage: main.py goodbye [OPTIONS] NAME

Options:
  --formal / --no-formal
  --help                  Show this message and exit.
```

Notice how it automatically creates a `--formal` and `--no-formal` for your `bool` *option*.

---

And of course, if you use it, it does what you expect:

```bash
python main.py hello Camila
```

shows:

```
Hello Camila
```

Then:

```bash
python main.py goodbye Camila
```

shows:

```
Bye Camila!
```

And:

```bash
python main.py goodbye --formal Camila
```

shows:

```
Goodbye Ms. Camila. Have a good day.
```

### Recap

In summary, you declare **once** the types of parameters (*arguments* and *options*) as function parameters.

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

And similarly for **files**, **paths**, **enums** (choices), etc. And there are tools to create **groups of sub-commands**, add metadata, extra **validation**, etc.

**You get**: great editor support, including **completion** and **type checks** everywhere.

**Your users get**: automatic **`--help`**, (optional) **autocompletion** in their terminal (Bash, Zsh, Fish, PowerShell).

For a more complete example including more features, see the <a href="https://typer.tiangolo.com/tutorial/intro/">Tutorial - User Guide</a>.

## Optional Dependencies

Typer uses <a href="https://click.palletsprojects.com/" target="_blank">Click</a> internally. That's the only dependency.

But you can install extras:

* <a href="https://pypi.org/project/colorama/" target="_blank"><code>colorama</code></a>: and Click will automatically use it to make sure colors always work correctly, even in Windows.
    * Then you can use any tool you want to output colors in all the systems, including the integrated `typer.style()` and `typer.secho()` (provided by Click).
    * Or any other tool, e.g. <a href="https://pypi.org/project/wasabi/" target="_blank"><code>wasabi</code></a>, <a href="https://github.com/erikrose/blessings" target="_blank"><code>blessings</code></a>.
* <a href="https://github.com/click-contrib/click-completion" target="_blank"><code>click-completion</code></a>: and Typer will automatically configure it to provide completion for all the shells, including installation commands.

You can install `typer` with `colorama` and `click-completion` with `pip3 install typer[all]`.

## Other tools and plug-ins

Click has many plug-ins available that you can use. And there are many tools that help with command line applications that you can use as well, even if they are not related to Typer or Click.

For example:

* <a href="https://github.com/click-contrib/click-spinner" target="_blank"><code>click-spinner</code></a>: to show the user that you are loading data. A Click plug-in.
    * * There are several other Click plug-ins at <a href="https://github.com/click-contrib" target="_blank">click-contrib</a> that you can explore.
* <a href="https://pypi.org/project/tabulate/" target="_blank"><code>tabulate</code></a>: to automatically display tabular data nicely. Independent of Click or typer.
* etc... you can re-use many of the great available tools for building CLIs.

## License

This project is licensed under the terms of the MIT license.
