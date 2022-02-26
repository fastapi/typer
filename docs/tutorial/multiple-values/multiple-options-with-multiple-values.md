You can also declare a *CLI option* that can be used multiple times and that has multiple values.

For example, let's say you want to accept several users with their first and last name in a single execution.

For this, use the standard Python `typing.List` to declare it as a `list` of `tuple[str, str]`:

```Python hl_lines="1  6"
{!../docs_src/multiple_values/multiple_options_with_multiple_values/tutorial001.py!}
```

You will receive the values as you declared them, as a `list` of `tuple[str, str]`.

Check it:

<div class="termy">

```console
$ python main.py

No provided users
Aborted!

// Now pass a user
$ python main.py --users Camila Evans

Processing user: Evans, Camila

// And now try with several users
$ python main.py --users Camila Evans --users Rick Evans

Processing user: Evans, Camila
Processing user: Evans, Rick
```

</div>
