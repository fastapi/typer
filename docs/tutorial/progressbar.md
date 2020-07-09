If you are executing an operation that can take some time, you can inform it to the user with a progress bar.

For this, you can use `typer.progressbar()`:

```Python hl_lines="8"
{!../docs_src/progressbar/tutorial001.py!}
```

You use `typer.progressbar()` with a `with` statement, as in:

```Python
with typer.progressbar(something) as progress:
    pass
```

And you pass as function argument to `typer.progressbar()` the thing that you would normally iterate over.

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

!!! tip
    Notice that there are 2 levels of code blocks. One for the `with` statement and one for the `for` statement.

!!! info
    This is mostly useful for operations that take some time.

    In the example above we are faking it with `time.sleep()`.

Check it:

<div class="termy">

```console
$ python main.py

---> 100%

Processed 100 things.
```

</div>

## Setting a Progress Bar `length`

The progress bar is generated from the length of the iterable (e.g. the list of users).

But if the length is not available (for example, with something that fetches a new user from a web API each time) you can pass an explicit `length` to `typer.progressbar()`.

```Python hl_lines="14"
{!../docs_src/progressbar/tutorial002.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

---> 100%

Processed 100 user IDs.
```

</div>

### About the function with `yield`

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

## Add a `label`

You can also set a `label`:

```Python hl_lines="8"
{!../docs_src/progressbar/tutorial003.py!}
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
{!../docs_src/progressbar/tutorial004.py!}
```

Check it:

<div class="use-termynal">
<span data-ty="input">python main.py</span>
<span data-ty="progress" data-ty-prompt="Batches"></span>
<span data-ty>Processed 100 things in batches.</span>
</div>
