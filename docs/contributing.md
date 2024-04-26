First, you might want to see the basic ways to [help Typer and get help](help-typer.md){.internal-link target=_blank}.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.

### Pre-commit hooks

We use <a href="https://pre-commit.com/" class="external-link" target="_blank">pre-commit</a> to run checks and formatting before submitting code for review.

#### Install pre-commit

We recommend <a href="https://pipx.pypa.io/" class="external-link" target="_blank">pipx</a> to install pre-commit in an isolated environment.

=== "pipx"

    <div class="termy">

    ```console
    $ pipx install pre-commit
    ```

    </div>

=== "pip"

    <div class="termy">

    ```console
    $ pip install pre-commit
    ```

    </div>

=== "Homebrew"

    <div class="termy">

    ```console
    $ brew install pre-commit
    ```

    </div>

=== "Conda"

    <div class="termy">

    ```console
    $ conda install pre-commit
    ```

    </div>

#### Activate hooks on the repository

By activating the hooks we instruct git to run the checks before every commit.

<div class="termy">

```console
$ pre-commit install
```

</div>

!!! note
    It's only needed once. From that point on, every time you commit, the pre-commit hooks will run, checking and formating the files you are committing.

#### Run checks manually

You can also manually run the checks on all files with:

<div class="termy">

```console
$ pre-commit run --all-files
```

</div>

### Virtual environment

You can create a virtual environment in a directory using Python's `venv` module:

<div class="termy">

```console
$ python -m venv env
```

</div>

That will create a directory `./env/` with the Python binaries and then you will be able to install packages for that isolated environment.

#### Activate the environment

Activate the new environment with:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ source ./env/bin/activate
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ .\env\Scripts\Activate.ps1
    ```

    </div>

=== "Windows Bash"

    Or if you use Bash for Windows (e.g. <a href="https://gitforwindows.org/" class="external-link" target="_blank">Git Bash</a>):

    <div class="termy">

    ```console
    $ source ./env/Scripts/activate
    ```

    </div>

To check it worked, use:

=== "Linux, macOS, Windows Bash"

    <div class="termy">

    ```console
    $ which pip

    some/directory/typer/env/bin/pip
    ```

    </div>

=== "Windows PowerShell"

    <div class="termy">

    ```console
    $ Get-Command pip

    some/directory/typer/env/bin/pip
    ```

    </div>

If it shows the `pip` binary at `env/bin/pip` then it worked. 🎉

!!! tip
    Every time you install a new package with `pip` under that environment, activate the environment again.

    This makes sure that if you use a terminal program installed by that package (like `flit`), you use the one from your local environment and not any other that could be installed globally.

### Install Typer

With the virtual environment activated, you can install Typer in "editable" mode:

<div class="termy">

```console
$ pip install --editable .
```

</div>

#### Using your local Typer

If you create a Python file that imports and uses Typer, and run it with the Python from your local environment, it will use your local Typer source code.

And if you update that local Typer source code, as it is installed with `--symlink` (or `--pth-file` on Windows), when you run that Python file again, it will use the fresh version of Typer you just edited.

That way, you don't have to "install" your local version to be able to test every change.

## Docs

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

Many of the tutorials have blocks of code.

In most of the cases, these blocks of code are actual complete applications that can be run as is.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs_src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

<div class="termy">

```console
$ bash scripts/docs-live.sh

<span style="color: green;">[INFO]</span>    -  Building documentation...
<span style="color: green;">[INFO]</span>    -  Cleaning site directory
<span style="color: green;">[INFO]</span>    -  Documentation built in 2.74 seconds
<span style="color: green;">[INFO]</span>    -  Serving on http://127.0.0.1:8008
```

</div>

It will serve the documentation on `http://127.0.0.1:8008`.

That way, you can edit the documentation/source files and see the changes live.

## Tests

Typer uses <a href="https://docs.pytest.org/" class="external-link" target="_blank">pytest</a> for testing.

Make sure you have the development dependencies installed:

<div class="termy">

```console
$ pip install -e requirements-tests.txt
```

</div>

### Running tests

To run the tests, you can use the `pytest` command:

<div class="termy">

```console
$ pytest -v
```

</div>

### Coverage report

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.
