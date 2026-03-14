# Building a Package

When you create a CLI program with **Typer** you probably want to create your own Python package.

That's what allows your users to install it and have it as an independent program that they can use in their terminal.

And that's also required for shell auto completion to work (unless you use your program through the `typer` command).

Nowadays, there are several ways and tools to create Python packages (what you install with `pip install something` or `uv add something`).

You might even have your favorite already.

Here's a very opinionated, short guide, showing one of the alternative ways of creating a Python package with a **Typer** app, from scratch.

/// tip

If you already have a favorite way of creating Python packages, feel free to skip this.

///

## Prerequisites

For this guide we'll use <a href="https://docs.astral.sh/uv/" class="external-link" target="_blank">uv</a>.

uv's docs are great, so go ahead, check them and install it.

## Create a project

Let's say we want to create a CLI application called `portal-gun`.

To make sure your package doesn't collide with the package created by someone else, we'll name it with a prefix of your name.

So, if your name is Rick, we'll call it `rick-portal-gun`.

Create a project with uv:

<div class="termy">

```console
$ uv init --package rick-portal-gun

Initialized project `rick-portal-gun` at `/home/rick-portal-gun`

// Enter the new project directory
cd ./rick-portal-gun
```

</div>

## Dependencies and environment

Add `typer` to your dependencies:

<div class="termy">

```console
$ uv add typer

// It creates a virtual environment for your project
Using CPython 3.14.0 interpreter at: /location/of/python/
Creating virtual environment at: .venv

Resolved 10 packages in 21ms
      Built rick-portal-gun @ file:/home/rick-portal-gun
Prepared 1 package in 19ms
Installed 10 packages in 34ms
 + click==8.3.1
 + colorama==0.4.6
 + markdown-it-py==4.0.0
 + mdurl==0.1.2
 + pygments==2.19.2
 + rich==14.2.0
 + rick-portal-gun==0.1.0 (from file:/home/rick-portal-gun)
 + shellingham==1.5.4
 + typer==0.21.0
 + typing-extensions==4.15.0


// Activate that new virtual environment
$ source .venv/bin/activate

// Open an editor using this new environment, for example VS Code
$ code ./
```

</div>

You can see that you have a generated project structure that looks like:

```
.
├── pyproject.toml
├── README.md
├── src
│   └── rick_portal_gun
│     └── __init__.py
└── uv.lock
```

## Create your app

Now let's create an extremely simple **Typer** app.

Create a file `src/rick_portal_gun/main.py` with:

```Python
import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
```

/// tip

As we are creating an installable Python package, there's no need to add a section with `if __name__ == "__main__":`.

///

## Modify the README

Let's change the README to have something like:

```Markdown
# Portal Gun

The awesome Portal Gun
```

## Add a "script"

We are creating a Python package that can be installed with `uv add` or `pip install`.

But we want it to provide a CLI program that can be executed in the shell.

To do that, we add a configuration to the `pyproject.toml` in the section `[project.scripts]`:

```TOML hl_lines="12 13"
[project]
name = "rick-portal-gun"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
authors = ["Rick Sanchez <rick@example.com>"]
requires-python = ">=3.14"
dependencies = [
    "typer>=0.21.0",
]

[project.scripts]
rick-portal-gun = "rick_portal_gun.main:app"

[build-system]
requires = ["uv_build>=0.8.14,<0.9.0"]
build-backend = "uv_build"
```

Here's what that line means:

`rick-portal-gun`: will be the name of the CLI program. That's how we will call it in the terminal once it is installed. Like:

<div class="termy">

```console
$ rick-portal-gun

// Something happens here ✨
```

</div>

`rick_portal_gun.main`, in the part `"rick_portal_gun.main:app"`, with underscores, refers to the Python module to import. That's what someone would use in a section like:

```Python
from rick_portal_gun.main import # something goes here
```

The `app` in `"rick_portal_gun.main:app"` is the thing to import from the module, and to call as a function, like:

```Python
from rick_portal_gun.main import app
app()
```

That config section tells uv that when this package is installed, we want it to create a command line program called `rick-portal-gun`.

And that the object to call (like a function) is the one in the variable `app` inside of the module `rick_portal_gun.main`.

## Install your package

That's what we need to create a package.

You can now install it:

<div class="termy">

```console
$ uv sync

Resolved 10 packages in 1ms
      Built rick-portal-gun @ file:/home/rick-portal-gun
Prepared 1 package in 18ms
Uninstalled 1 package in 1ms
Installed 1 package in 13ms
 ~ rick-portal-gun==0.1.0 (from file:/home/rick-portal-gun)

```

</div>

## Try your CLI program

Your package is installed in the environment created by uv, but you can already use it.

<div class="termy">

```console
// You can use the which program to check which rick-portal-gun program is available (if any)
$ which rick-portal-gun

// You get the one from your environment
/home/rick-portal-gun/.venv/bin/rick-portal-gun

// Try it
$ rick-portal-gun --help

// You get all the standard help
Usage: rick-portal-gun [OPTIONS] COMMAND [ARGS]...

  Awesome Portal Gun

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.

  --help                Show this message and exit.

Commands:
  shoot  Shoot the portal gun
  load   Load the portal gun
```

</div>

## Create a wheel package

Python packages have a standard format called a "wheel". It's a file that ends in `.whl`.

You can create a wheel with uv:

<div class="termy">

```console
$ uv build

Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built dist/rick_portal_gun-0.1.0.tar.gz
Successfully built dist/rick_portal_gun-0.1.0-py3-none-any.whl
```

</div>

After that, if you check in your project directory, you should now have a couple of extra files at `./dist/`:

``` hl_lines="3 4"
.
├── dist
│   ├── rick_portal_gun-0.1.0-py3-none-any.whl
│   └── rick-portal-gun-0.1.0.tar.gz
├── pyproject.toml
├── README.md
├── ...
```

The `.whl` is the wheel file. You can send that wheel file to anyone and they can use it to install your program (we'll see how to upload it to PyPI in a bit).

## Test your wheel package

Now you can open another terminal and install that package from the file for your own user with:

<div class="termy">

```console
$ pip install --user /home/rick/rick-portal-gun/dist/rick_portal_gun-0.1.0-py3-none-any.whl

---> 100%
```

</div>

/// warning

The `--user` is important, that ensures you install it in your user's directory and not in the global system.

If you installed it in the global system (e.g. with `sudo`) you could install a version of a library (e.g. a sub-dependency) that is incompatible with your system.

///

/// tip

Bonus points if you use <a href="https://docs.astral.sh/uv/" class="external-link" target="_blank">uvx</a> to install it while keeping an isolated environment for your Python CLI programs 🚀

///

Now you have your CLI program installed. And you can use it freely:

<div class="termy">

```console
$ rick-portal-gun shoot

// It works 🎉
Shooting portal gun
```

</div>

Having it installed globally (and not in a single environment), you can now install completion globally for it:

<div class="termy">

```console
$ rick-portal-gun --install-completion

zsh completion installed in /home/rick/.zshrc.
Completion will take effect once you restart the terminal.
```

</div>

/// tip

If you want to remove completion you can just delete the added line in that file.

///

And after you restart the terminal you will get completion for your new CLI program:

<div class="termy">

```console
$ rick-portal-gun [TAB][TAB]

// You get completion for your CLI program ✨
load   -- Load the portal gun
shoot  -- Shoot the portal gun
```

</div>

## Support `python -m` (optional)

You may have seen that you can call many Python modules as scripts with `python -m some-module`.

For example, one way to call `pip` is:

<div class="termy">

```console
$ pip install fastapi
```

</div>

But you can also call Python with the `-m` *CLI Option* and pass a module for it to execute as if it was a script, like:

<div class="termy">

```console
$ python -m pip install fastapi
```

</div>

Here we pass `pip` as the value for `-m`, so, Python will execute the module `pip` as if it was a script. And then it will pass the rest of the *CLI Parameters* (`install fastapi`) to it.

These two are more or less equivalent, the `install fastapi` will be passed to `pip`.

/// tip

In the case of `pip`, in many occasions it's actually recommended that you run it with `python -m`, because if you create a virtual environment with its own `python`, that will ensure that you use the `pip` from *that* environment.

///

### Add a `__main__.py`

You can support that same style of calling the package/module for your own package, simply by adding a file `__main__.py`.

Python will look for that file and execute it.

The file would live right beside `__init__.py` and `main.py`:

``` hl_lines="7"
.
├── pyproject.toml
├── README.md
├── src
│   └── rick_portal_gun
│     ├── __init__.py
│     ├── __main__.py
│     └── main.py
└── uv.lock
```

No other file has to import it, you don't have to reference it in your `pyproject.toml` or anything else, it just works by default, as it is standard Python behavior.

Then in that file you can execute your **Typer** program:

```Python
from .main import app
app()
```

Now, after installing your package, if you call it with `python -m` it will work:

<div class="termy">

```console
$ python -m rick_portal_gun --help

Usage: python -m rick_portal_gun [OPTIONS] COMMAND [ARGS]...

  Awesome Portal Gun

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.

  --help                Show this message and exit.

Commands:
  shoot  Shoot the portal gun
  load   Load the portal gun
```

</div>

/// tip

Notice that you have to pass the importable version of the package name, so `rick_portal_gun` instead of `rick-portal-gun`.

///

That works! 🚀

### Autocompletion and `python -m`

Have in mind that TAB completion (shell auto-completion) won't work when using `python -m`.

Auto-completion depends on the name of the program called, it's tied to each specific program name.

So, to have shell completion for `rick-portal-gun` you would have to call it directly:

<div class="termy">

```console
$ rick-portal-gun [TAB][TAB]
```

</div>

But you can still support `python -m` for the cases where it's useful.

## Publish to PyPI (optional)

You can publish that new package to <a href="https://pypi.org/" class="external-link" target="_blank">PyPI</a> to make it public, so others can install it easily.

So, go ahead and create an account there (it's free).

### PyPI API token

To do it, you first need to configure a PyPI auth token.

Login to <a href="https://pypi.org/" class="external-link" target="_blank">PyPI</a>.

And then go to <a href="https://pypi.org/manage/account/token/" class="external-link" target="_blank">https://pypi.org/manage/account/token/</a> to create a new token.

Let's say your new API token is:

```
pypi-wubalubadubdub-deadbeef1234
```

Now configure uv to use this token by setting an environment variable:

<div class="termy">

```console
$ export UV_PUBLISH_TOKEN=pypi-wubalubadubdub-deadbeef1234
// It won't show any output, but it's already configured
```

</div>

### Publish to PyPI

Now you can publish your package.

<div class="termy">

```console
$ uv publish

Publishing 2 files https://upload.pypi.org/legacy/
Uploading rick_portal_gun-0.1.0-py3-none-any.whl (2.3KiB)
Uploading rick_portal_gun-0.1.0.tar.gz (841.0B)
```

</div>

Now you can go to PyPI and check your projects at <a href="https://pypi.org/manage/projects/" class="external-link" target="_blank">https://pypi.org/manage/projects/</a>.

You should now see your new "rick-portal-gun" package.

### Install from PyPI

Now to see that we can install it from PyPI, open another terminal, and uninstall the currently installed package.

<div class="termy">

```console
$ pip uninstall rick-portal-gun

Found existing installation: rick-portal-gun 0.1.0
Uninstalling rick-portal-gun-0.1.0:
  Would remove:
    /home/rick/.local/bin/rick-portal-gun
    /home/rick/.local/lib/python3.10/site-packages/rick_portal_gun-0.1.0.dist-info/*
    /home/rick/.local/lib/python3.10/site-packages/rick_portal_gun/*
# Proceed (Y/n)? $ Y
    Successfully uninstalled rick-portal-gun-0.1.0
```

</div>

And now install it again, but this time using just the name, so that `pip` pulls it from PyPI:

<div class="termy">

```console
$ pip install --user rick-portal-gun

// Notice that it says "Downloading" 🚀
Collecting rick-portal-gun
  Downloading rick_portal_gun-0.1.0-py3-none-any.whl.metadata (435 bytes)
Requirement already satisfied: typer<0.13.0,>=0.12.3 in ./.local/lib/python3.10/site-packages (from rick-portal-gun==0.1.0) (0.12.3)
Requirement already satisfied: typing-extensions>=3.7.4.3 in ./.local/lib/python3.10/site-packages (from typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (4.11.0)
Requirement already satisfied: click>=8.0.0 in ./.local/lib/python3.10/site-packages (from typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (8.1.7)
Requirement already satisfied: shellingham>=1.3.0 in ./.local/lib/python3.10/site-packages (from typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (1.5.4)
Requirement already satisfied: rich>=10.11.0 in ./.local/lib/python3.10/site-packages (from typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (13.7.1)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in ./.local/lib/python3.10/site-packages (from rich>=10.11.0->typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (2.17.2)
Requirement already satisfied: markdown-it-py>=2.2.0 in ./.local/lib/python3.10/site-packages (from rich>=10.11.0->typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (3.0.0)
Requirement already satisfied: mdurl~=0.1 in ./.local/lib/python3.10/site-packages (from markdown-it-py>=2.2.0->rich>=10.11.0->typer<0.13.0,>=0.12.3->rick-portal-gun==0.1.0) (0.1.2)
Downloading rick_portal_gun-0.1.0-py3-none-any.whl (1.8 kB)
Installing collected packages: rick-portal-gun
Successfully installed rick-portal-gun-0.1.0
```

</div>

And now test the newly installed package from PyPI:

<div class="termy">

```console
$ rick-portal-gun load

// It works! 🎉
Loading portal gun
```

</div>

## Generate docs

You can use the `typer` command to generate docs for your package that you can put in your `README.md`:

<div class="termy">

```console
$ typer rick_portal_gun.main utils docs --output README.md --name rick-portal-gun

Docs saved to: README.md
```

</div>

You just have to pass it the module to import (`rick_portal_gun.main`) and it will detect the `typer.Typer` app automatically.

By specifying the `--name` of the program it will be able to use it while generating the docs.

### Publish a new version with the docs

Now you can publish a new version with the updated docs.

For that you need to first increase the version in `pyproject.toml`:

```TOML hl_lines="3"
[project]
name = "rick-portal-gun"
version = "0.2.0"
description = "Add your description here"
readme = "README.md"
authors = ["Rick Sanchez <rick@example.com>"]
requires-python = ">=3.14"
dependencies = [
    "typer>=0.21.0",
]

[project.scripts]
rick-portal-gun = "rick_portal_gun.main:app"

[build-system]
requires = ["uv_build>=0.8.14,<0.9.0"]
build-backend = "uv_build"
```

And then build and publish again:

<div class="termy">

```console
$ uv build
$ uv publish

Publishing 2 files https://upload.pypi.org/legacy/
Uploading rick_portal_gun-0.2.0-py3-none-any.whl (2.3KiB)
Uploading rick_portal_gun-0.2.0.tar.gz (840.0B)
```

</div>

And now you can go to PyPI, to the project page, and reload it, and it will now have your new generated docs.

## What's next

This is a very simple guide. You could add many more steps.

For example, you should use <a href="https://git-scm.com/" class="external-link" target="_blank">Git</a>, the version control system, to save your code.

You could use <a href="https://docs.astral.sh/uv/" class="external-link" target="_blank">uv</a> to manage your installed CLI Python programs in isolated environments.

Maybe use automatic formatting with <a href="https://docs.astral.sh/ruff/" class="external-link" target="_blank">Ruff</a>.

You'll probably want to publish your code as open source to <a href="https://github.com/" class="external-link" target="_blank">GitHub</a>.

And then you could integrate a <abbr title="Continuous Integration">CI</abbr> tool to run your tests and deploy your package automatically.

And there's a long etc. But now you have the basics and you can continue on your own. 🚀
