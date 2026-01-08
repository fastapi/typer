# Multiple options with multiple values

For when simple doesn't quite cut it, you may also declare a *CLI option* that takes several values of different types and can be used multiple times.

For this, we use the standard Python `list` and declare it as a list of `tuple`:

{* docs_src/multiple_values/multiple_options_with_multiple_values/tutorial001_an_py39.py hl[9] *}

Just as before, the types internal to the `tuple` define the type of each value in the tuple.

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
