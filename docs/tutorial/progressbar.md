# Progress Bar

If you are executing an operation that can take some time, you can inform it to the user. 🤓

## Progress Bar

You can use <a href="https://rich.readthedocs.io/en/stable/progress.html" class="external-link" target="_blank">Rich's Progress Display</a> to show a progress bar, for example:

```Python hl_lines="4  9"
{!../docs_src/progressbar/tutorial001.py!}
```

You put the thing that you want to iterate over inside of Rich's `track()`, and then iterate over that.

Check it:

<div class="termy">

```console
$ python main.py

---> 100%

Processed 100 things.
```

</div>

...actually, it will look a lot prettier. ✨ But I can't show you the animation here in the docs. 😅

The colors and information will look something like this:

<div class="termy">

```console
$ python main.py

Processing... <font color="#F92672">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╸</font><font color="#3A3A3A">━━━━━━━━━━</font> <font color="#AE81FF"> 74%</font> <font color="#A1EFE4">0:00:01</font>
```

</div>

## Spinner

When you don't know how long the operation will take, you can use a spinner instead.

Rich allows you to display many things in complex and advanced ways.

For example, this will show two spinners:

```Python hl_lines="4  8-15"
{!../docs_src/progressbar/tutorial002.py!}
```

I can't show you the beautiful animation here in the docs. 😅

But at some point in time it will look like this (imagine it's spinning). 🤓

<div class="termy">

```console
$ python main.py

<font color="#A6E22E">⠹</font> Processing...
<font color="#A6E22E">⠹</font> Preparing...
```

</div>

You can learn more about it in the <a href="https://rich.readthedocs.io/en/stable/progress.html" class="external-link" target="_blank">Rich docs for Progress Display</a>.

## Typer `progressbar`

If you can, you should use **Rich** as explained above, it has more features, it's more advanced, and can display information more beautifully. ✨

/// tip

If you can use Rich, use the information above, the Rich docs, and skip the rest of this page. 😎

///

But if you can't use Rich, Typer (actually Click) comes with a simple utility to show progress bars.

/// info

`typer.progressbar()` comes directly from Click, you can read more about it in <a href="https://click.palletsprojects.com/en/8.1.x/utils/#showing-progress-bars" class="external-link" target="_blank">Click's docs</a>.

///

### Use `typer.progressbar`

/// tip

Remember, you are much better off using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> for this. 😎

///

You can use `typer.progressbar()` with a `with` statement, as in:

```Python
with typer.progressbar(something) as progress:
    pass
```

And you pass as function argument to `typer.progressbar()` the thing that you would normally iterate over.

```Python hl_lines="8"
{!../docs_src/progressbar/tutorial003.py!}
```

So, if you have a list of users, this could be:

```Python
users = ["Camila", "Rick", "Morty"]

with typer.progressbar(users) as progress:
    pass
```

And the `with` statement using `typer.progressbar()` gives you an object that you can iterate over, just like if it was the same thing that you would iterate over normally.

But by iterating over this object **Typer** (actually Click) will know to update the progress bar:

```Python
users = ["Camila", "Rick", "Morty"]

with typer.progressbar(users) as progress:
    for user in progress:
        typer.echo(user)
```

/// tip

Notice that there are 2 levels of code blocks. One for the `with` statement and one for the `for` statement.

///

/// info

This is mostly useful for operations that take some time.

In the example above we are faking it with `time.sleep()`.

///

Check it:

<div class="termy">

```console
$ python main.py

---> 100%

Processed 100 things.
```

</div>

### Setting a Progress Bar `length`

/// tip

Remember, you are much better off using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> for this. 😎

///

The progress bar is generated from the length of the iterable (e.g. the list of users).

But if the length is not available (for example, with something that fetches a new user from a web API each time) you can pass an explicit `length` to `typer.progressbar()`.

```Python hl_lines="14"
{!../docs_src/progressbar/tutorial004.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

---> 100%

Processed 100 user IDs.
```

</div>

#### About the function with `yield`

If you hadn't seen something like that `yield` above, that's a "<a href="https://docs.python.org/3/glossary.html#term-generator" class="external-link" target="_blank">generator</a>".

You can iterate over that function with a `for` and at each iteration it will give you the value at `yield`.

`yield` is like a `return` that gives values multiple times and let's you use the function in a `for` loop.

For example:

```Python
def iterate_user_ids():
    # Let's imagine this is a web API, not a range()
    for i in range(100):
        yield i

for i in iterate_user_ids():
    print(i)
```

would print each of the "user IDs" (here it's just the numbers from `0` to `99`).

### Add a `label`

/// tip

Remember, you are much better off using <a href="https://rich.readthedocs.io/" class="external-link" target="_blank">Rich</a> for this. 😎

///

You can also set a `label`:

```Python hl_lines="8"
{!../docs_src/progressbar/tutorial005.py!}
```

Check it:

<div class="use-termynal">
<span data-ty="input">python main.py</span>
<span data-ty="progress" data-ty-prompt="Processing"></span>
<span data-ty>Processed 100 things.</span>
</div>

## Iterate manually

If you need to manually iterate over something and update the progress bar irregularly, you can do it by not passing an iterable but just a `length` to `typer.progressbar()`.

And then calling the `.update()` method in the object from the `with` statement:

```Python hl_lines="8  12"
{!../docs_src/progressbar/tutorial006.py!}
```

Check it:

<div class="use-termynal">
<span data-ty="input">python main.py</span>
<span data-ty="progress" data-ty-prompt="Batches"></span>
<span data-ty>Processed 1000 things in batches.</span>
</div>
