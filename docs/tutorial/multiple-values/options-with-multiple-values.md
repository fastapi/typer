# CLI Options with Multiple Values

You can also declare a *CLI option* that takes several values of different types.

You can set the number of values and types to anything you want, but it has to be a fixed number of values.

For this, use the standard Python `typing.Tuple`:

//// tab | Python 3.7+

```Python hl_lines="1  7"
{!> ../docs_src/multiple_values/options_with_multiple_values/tutorial001_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="1  6"
{!> ../docs_src/multiple_values/options_with_multiple_values/tutorial001.py!}
```

////

Each of the internal types defines the type of each value in the tuple.

So:

```Python
user: Tuple[str, int, bool]
```

means that the parameter `user` is a tuple of 3 values.

* The first value is a `str`.
* The second value is an `int`.
* The third value is a `bool`.

Later we do:

```Python
username, coins, is_wizard = user
```

If you hadn't seen that, it means that `user` is a tuple with 3 values, and we are assigning each of the values to a new variable:

* The first value in the tuple `user` (a `str`) goes to the variable `username`.
* The second value in the tuple `user` (an `int`) goes to the variable `coins`.
* The third value in the tuple `user` (a `bool`) goes to the variable `is_wizard`.

So, this:

```Python
username, coins, is_wizard = user
```

is equivalent to this:

```Python
username = user[0]
coins = user[1]
is_wizard = user[2]
```

/// tip

Notice that the default is a tuple with `(None, None, None)`.

You cannot simply use `None` here as the default because <a href="https://github.com/pallets/click/issues/472" class="external-link" target="_blank">Click doesn't support it</a>.

///

## Check it

Now let's see how this works in the terminal:

<div class="termy">

```console
// check the help
$ python main.py --help

// Notice the &lt;TEXT INTEGER BOOLEAN&gt;
Usage: main.py [OPTIONS]

Options:
  --user &lt;TEXT INTEGER BOOLEAN&gt;...
  --help                          Show this message and exit.

// Now try it
$ python main.py --user Camila 50 yes

The username Camila has 50 coins
And this user is a wizard!

// With other values
$ python main.py --user Morty 3 no

The username Morty has 3 coins

// Try with invalid values (not enough)
$ python main.py --user Camila 50

Error: Option '--user' requires 3 arguments
```

</div>
