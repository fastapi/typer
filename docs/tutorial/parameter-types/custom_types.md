You can easily expand **Typer**'s parameter parsing to support your own types.

Two interfaces are available for expanding parameter parsing:

1. [Providing a callable to parse the text](#callable-parser)
1. [Expanding Click's type parsers](#click-type-parser)

## Callable Parser

`typer.Argument` and `typer.Option` can create custom parameter types with a `parser` callable.


```Python hl_lines="12-13  17  18"
{!../docs_src/parameter_types/custom_types/tutorial001.py!}
```

## Click Type Parser

If you already have a Click type parser define for your type, `typer.Argument` and `typer.Option`
can use it with the `click_type` option.

```Python hl_lines="13-17  21  22"
{!../docs_src/parameter_types/custom_types/tutorial002.py!}
```
