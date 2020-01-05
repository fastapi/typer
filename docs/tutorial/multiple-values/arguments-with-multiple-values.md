*CLI arguments* can also receive multiple values.

You can define the type of a *CLI argument* using `typing.List`.

```Python hl_lines="7"
{!./src/multiple_values/arguments_with_multiple_values/tutorial001.py!}
```

And then you can pass it as many *CLI arguments* of that type as you want:

<div class="termy">

```console
$ python main.py ./index.md ./first-steps.md woohoo!

This file exists: index.md
woohoo!
This file exists: first-steps.md
woohoo!
```

</div>

!!! tip
    We also declared a final *CLI argument* `celebration`, and it's correctly used even if we pass an arbitrary number of `files` first.

!!! info
    A `List` can only be used in the last command (if there are subcommands), as this will take anything to the right and assume it's part of the expected *CLI arguments*.
