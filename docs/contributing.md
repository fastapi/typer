# Development - Contributing

First, you might want to see the basic ways to [help Typer and get help](help-typer.md){.internal-link target=_blank}.

## Developing

If you already cloned the <a href="https://github.com/fastapi/typer" class="external-link" target="_blank">typer repository</a> and you want to deep dive in the code, here are some guidelines to set up your environment.

### Virtual Environment

Follow the instructions to create and activate a [virtual environment](virtual-environments.md){.internal-link target=_blank} for the internal code of `typer`.

### Install Requirements Using `pip`

After activating the environment, install the required packages:

<div class="termy">

```console
$ pip install -r requirements.txt

---> 100%
```

</div>

It will install all the dependencies and your local Typer in your local environment.

### Using your Local Typer

If you create a Python file that imports and uses Typer, and run it with the Python from your local environment, it will use your cloned local Typer source code.

And if you update that local Typer source code when you run that Python file again, it will use the fresh version of Typer you just edited.

That way, you don't have to "install" your local version to be able to test every change.

/// note | "Technical Details"

This only happens when you install using this included `requirements.txt` instead of running `pip install typer` directly.

That is because inside the `requirements.txt` file, the local version of Typer is marked to be installed in "editable" mode, with the `-e` option.

///

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

## Tests

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

### Docs live

During local development, there is a script that builds the site and checks for any changes, live-reloading:

<div class="termy">

```console
$ python ./scripts/docs.py live

<span style="color: green;">[INFO]</span> Serving on http://127.0.0.1:8008
<span style="color: green;">[INFO]</span> Start watching changes
<span style="color: green;">[INFO]</span> Start detecting changes
```

</div>

It will serve the documentation on `http://127.0.0.1:8008`.

That way, you can edit the documentation/source files and see the changes live.

/// tip

Alternatively, you can perform the same steps that scripts does manually.

Go into the docs director at `docs/`:

```console
$ cd docs/
```

Then run `mkdocs` in that directory:

```console
$ mkdocs serve --dev-addr 8008
```

///

#### Typer CLI (optional)

The instructions here show you how to use the script at `./scripts/docs.py` with the `python` program directly.

But you can also use <a href="https://typer.tiangolo.com/typer-cli/" class="external-link" target="_blank">Typer CLI</a>, and you will get autocompletion in your terminal for the commands after installing completion.

If you install Typer CLI, you can install completion with:

<div class="termy">

```console
$ typer --install-completion

zsh completion installed in /home/user/.bashrc.
Completion will take effect once you restart the terminal.
```

</div>

### Docs Structure

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

And there are extra tools/scripts in place in `./scripts/docs.py`.

/// tip

You don't need to see the code in `./scripts/docs.py`, you just use it in the command line.

///

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for Tests

Most of the tests actually run against the example source files in the documentation.

This helps to make sure that:

* The documentation is up-to-date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.
