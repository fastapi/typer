You can declare a *CLI option* that can be used multiple times, and then get all the values.

For example, let's say you want to accept several users in a single execution.

For this, use the standard Python `typing.List` to declare it as a `list` of `str`:

```Python hl_lines="1  6"
{!../docs_src/multiple_values/multiple_options/tutorial001.py!}
```

You will receive the values as you declared them, as a `list` of `str`.

Check it:

<div class="termy">

```console
$ python main.py

No provided users
Aborted!

// Now pass a user
$ python main.py --user Camila

Processing user: Camila

// And now try with several users
$ python main.py --user Camila --user Rick --user Morty

Processing user: Camila
Processing user: Rick
Processing user: Morty
```

</div>

## Multiple `float`

The same way, you can use other types and they will be converted by **Typer** to their declared type:

```Python hl_lines="6"
{!../docs_src/multiple_values/multiple_options/tutorial002.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

The sum is 0

// Try with some numbers
$ python main.py --number 2

The sum is 2.0

// Try with some numbers
$ python main.py --number 2 --number 3 --number 4.5

The sum is 9.5
```

</div>
