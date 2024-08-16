For when simple doesn't quite cut it, you may also declare a *CLI option* that takes several values of different types and can be used multiple times.

The same rules apply for the number of values for each use and their types; the types may be anything you want, but there must be a fixed number of values.

For this, we use the standard Python `typing.List` and declare its internal type to be a `typing.Tuple`:

//// tab | Python 3.7+

```Python hl_lines="1  7"
{!> ../docs_src/multiple_values/multiple_options_with_multiple_values/tutorial001_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible

///

```Python hl_lines="1  6"
{!> ../docs_src/multiple_values/multiple_options_with_multiple_values/tutorial001.py!}
```

////

Just as before, the types internal to the `Tuple` define the type of each value in the tuple.

## Check it

<div class="termy">

```console
$ python main.py

Congratulations, you're debt-free!

// Now let's borrow some money.
$ python main.py --borrow 2.5 Mark

Borrowed 2.50 from Mark

Total borrowed: 2.50

// And, of course, it may be used multiple times
$ python main.py --borrow 2.5 Mark --borrow 5.25 Sean --borrow 1.75 Wade

Borrowed 2.50 from Mark
Borrowed 5.25 from Sean
Borrowed 1.75 from Wade

Total borrowed: 9.50
```

</div>
