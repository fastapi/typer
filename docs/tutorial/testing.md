# Testing

Testing **Typer** applications is very easy with <a href="https://docs.pytest.org/en/latest/" class="external-link" target="_blank">pytest</a>.

Let's say you have an application `app/main.py` with:

```Python
{!../docs_src/testing/app01/main.py!}
```

So, you would use it like:

<div class="termy">

```console
$ python main.py Camila --city Berlin

Hello Camila
Let's have a coffee in Berlin
```

</div>

And the directory also has an empty `app/__init__.py` file.

So, the `app` is a "Python package".

## Test the app

### Import and create a `CliRunner`

Create another file/module `app/test_main.py`.

Import `CliRunner` and create a `runner` object.

This runner is what will "invoke" or "call" your command line application.

```Python hl_lines="1  5"
{!../docs_src/testing/app01/test_main.py!}
```

/// tip

It's important that the name of the file starts with `test_`, that way pytest will be able to detect it and use it automatically.

///

### Call the app

Then create a function `test_app()`.

And inside of the function, use the `runner` to `invoke` the application.

The first parameter to `runner.invoke()` is a `Typer` app.

The second parameter is a `list` of `str`, with all the text you would pass in the command line, right as you would pass it:

```Python hl_lines="8 9"
{!../docs_src/testing/app01/test_main.py!}
```

/// tip

The name of the function has to start with `test_`, that way pytest can detect it and use it automatically.

///

### Check the result

Then, inside of the test function, add `assert` statements to ensure that everything in the result of the call is as it should be.

```Python hl_lines="10 11 12"
{!../docs_src/testing/app01/test_main.py!}
```

Here we are checking that the exit code is 0, as it is for programs that exit without errors.

Then we check that the text printed to "standard output" contains the text that our CLI program prints.

/// tip

You could also check `result.stderr` for "standard error" independently from "standard output" if your `CliRunner` instance is created with the `mix_stderr=False` argument.

///

/// info

If you need a refresher about what is "standard output" and "standard error" check the section in [Printing and Colors: "Standard Output" and "Standard Error"](printing.md#standard-output-and-standard-error){.internal-link target=_blank}.

///

### Call `pytest`

Then you can call `pytest` in your directory and it will run your tests:

<div class="termy">

```console
$ pytest

================ test session starts ================
platform linux -- Python 3.10, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/user/code/superawesome-cli/app
plugins: forked-1.1.3, xdist-1.31.0, cov-2.8.1
collected 1 item

---> 100%

test_main.py <span style="color: green; white-space: pre;">.                                 [100%]</span>

<span style="color: green;">================= 1 passed in 0.03s =================</span>
```

</div>

## Testing input

If you have a CLI with prompts, like:

//// tab | Python 3.7+

```Python hl_lines="8"
{!> ../docs_src/testing/app02_an/main.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="7"
{!> ../docs_src/testing/app02/main.py!}
```

////

That you would use like:

<div class="termy">

```console
$ python main.py Camila

# Email: $ camila@example.com

Hello Camila, your email is: camila@example.com
```

</div>

You can test the input typed in the terminal using `input="camila@example.com\n"`.

This is because what you type in the terminal goes to "**standard input**" and is handled by the operating system as if it was a "virtual file".

/// info

If you need a refresher about what is "standard output", "standard error", and "standard input" check the section in [Printing and Colors: "Standard Output" and "Standard Error"](printing.md#standard-output-and-standard-error){.internal-link target=_blank}.

///

When you hit the <kbd>ENTER</kbd> key after typing the email, that is just a "new line character". And in Python that is represented with `"\n"`.

So, if you use `input="camila@example.com\n"` it means: "type `camila@example.com` in the terminal, then hit the <kbd>ENTER</kbd> key":

```Python hl_lines="9"
{!../docs_src/testing/app02/test_main.py!}
```

## Test a function

If you have a script and you never created an explicit `typer.Typer` app, like:

```Python hl_lines="9"
{!../docs_src/testing/app03/main.py!}
```

...you can still test it, by creating an app during testing:

```Python hl_lines="6 7  13"
{!../docs_src/testing/app03/test_main.py!}
```

Of course, if you are testing that script, it's probably easier/cleaner to just create the explicit `typer.Typer` app in `main.py` instead of creating it just during the test.

But if you want to keep it that way, e.g. because it's a simple example in documentation, then you can use that trick.

### About the `app.command` decorator

Notice the `app.command()(main)`.

If it's not obvious what it's doing, continue reading...

You would normally write something like:

```Python
@app.command()
def main(name: str = "World"):
    # Some code here
```

But `@app.command()` is just a decorator.

That's equivalent to:

```Python
def main(name: str = "World"):
    # Some code here

decorator = app.command()

new_main = decorator(main)
main = new_main
```

`app.command()` returns a function (`decorator`) that takes another function as it's only parameter (`main`).

And by using the `@something` you normally tell Python to replace the thing below (the function `main`) with the return of the `decorator` function (`new_main`).

Now, in the specific case of **Typer**, the decorator doesn't change the original function. It registers it internally and returns it unmodified.

So, `new_main` is actually the same original `main`.

So, in the case of **Typer**, as it doesn't really modify the decorated function, that would be equivalent to:

```Python
def main(name: str = "World"):
    # Some code here

decorator = app.command()

decorator(main)
```

But then we don't need to create the variable `decorator` to use it below, we can just use it directly:

```Python
def main(name: str = "World"):
    # Some code here

app.command()(main)
```

...that's it. It's still probably simpler to just create the explicit `typer.Typer` in the `main.py` file 😅.
