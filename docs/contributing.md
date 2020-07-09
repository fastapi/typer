First, you might want to see the basic ways to [help Typer and get help](help-typer.md){.internal-link target=_blank}.

## Developing

If you already cloned the repository and you know that you need to deep dive in the code, here are some guidelines to set up your environment.

### Virtual environment with `venv`

You can create a virtual environment in a directory using Python's `venv` module:

<div class="termy">

```console
$ python -m venv env
```

</div>

That will create a directory `./env/` with the Python binaries and then you will be able to install packages for that isolated environment.

### Activate the environment

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

### Flit

**Typer** uses <a href="https://flit.readthedocs.io/en/latest/index.html" class="external-link" target="_blank">Flit</a> to build, package and publish the project.

After activating the environment as described above, install `flit`:

<div class="termy">

```console
$ pip install flit

---> 100%
```

</div>

Now re-activate the environment to make sure you are using the `flit` you just installed (and not a global one).

And now use `flit` to install the development dependencies:

=== "Linux, macOS"

    <div class="termy">

    ```console
    $ flit install --deps develop --symlink

    ---> 100%
    ```

    </div>

=== "Windows"

    If you are on Windows, use `--pth-file` instead of `--symlink`:

    <div class="termy">

    ```console
    $ flit install --deps develop --pth-file

    ---> 100%
    ```

    </div>

It will install all the dependencies and your local Typer in your local environment.

#### Using your local Typer

If you create a Python file that imports and uses Typer, and run it with the Python from your local environment, it will use your local Typer source code.

And if you update that local Typer source code, as it is installed with `--symlink` (or `--pth-file` on Windows), when you run that Python file again, it will use the fresh version of Typer you just edited.

That way, you don't have to "install" your local version to be able to test every change.

### Format

There is a script that you can run that will format and clean all your code:

<div class="termy">

```console
$ bash scripts/format.sh
```

</div>

It will also auto-sort all your imports.

For it to sort them correctly, you need to have Typer installed locally in your environment, with the command in the section above using `--symlink` (or `--pth-file` on Windows).

### Format imports

There is another script that formats all the imports and makes sure you don't have unused imports:

<div class="termy">

```console
$ bash scripts/format-imports.sh
```

</div>

As it runs one command after the other and modifies and reverts many files, it takes a bit longer to run, so it might be easier to use `scripts/format.sh` frequently and `scripts/format-imports.sh` only before committing.

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

There is a script that you can run locally to test all the code and generate coverage reports in HTML:

<div class="termy">

```console
$ bash scripts/test-cov-html.sh
```

</div>

This command generates a directory `./htmlcov/`, if you open the file `./htmlcov/index.html` in your browser, you can explore interactively the regions of code that are covered by the tests, and notice if there is any region missing.
