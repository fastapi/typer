You can declare a *CLI option* that can be used multiple times, and then get all the values.

For example, let's say you want to accept several users in a single execution.

For this, use the standard Python `typing.List` to declare it as a `list` of `str`:

=== "Python 3.7+"

    ```Python hl_lines="1  7"
    {!> ../docs_src/multiple_values/multiple_options/tutorial001_an.py!}
    ```

=== "Python 3.7+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="1  6"
    {!> ../docs_src/multiple_values/multiple_options/tutorial001.py!}
    ```

You will receive the values as you declared them, as a `list` of `str`.

Check it:

<div class="termy">

```console
// The default value is 'None'
$ python main.py

No provided users (raw input = None)
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

=== "Python 3.7+"

    ```Python hl_lines="7"
    {!> ../docs_src/multiple_values/multiple_options/tutorial002_an.py!}
    ```

=== "Python 3.7+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="6"
    {!> ../docs_src/multiple_values/multiple_options/tutorial002.py!}
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

## Passing multiple values in a single argument

Many users expect to be able to pass multiple arguments with a single .
**Typer** supports this with the `separator` option for `typing.List[T]` types:

=== "Python 3.7+"

    ```Python hl_lines="7"
    {!> ../docs_src/multiple_values/multiple_options/tutorial003_an.py!}
    ```

=== "Python 3.7+ non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="6"
    {!> ../docs_src/multiple_values/multiple_options/tutorial003.py!}
    ```

Check it:

<div class="termy">

```console
$ python main.py

The sum is 0

// Behaves
$ python main.py --number 2

The sum is 2.0

// Values to the argument are split using the passed separator
$ python main.py --number "2, 3, 4.5"

// Supports passing the option multiple times. This joins all values to a single list
$ python main.py --number "2, 3, 4.5" --number 5

The sum is 14.5
```

</div>

!!! warning
    Only single-character non-whitespace separators are supported. Note that passing `--number 2, 3, 4.5` (without wrapping the value in "") does not work.
