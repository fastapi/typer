# Custom Types

You can easily use your own custom types in your **Typer** applications.

The way to do it is by providing a way to <abbr title="convert from some plain format, like the input text in the CLI, into Python objects">parse</abbr> input into your own types.

There are two ways to achieve this:

* Adding a type `parser`
* Expanding Click's custom types

## Type Parser

`typer.Argument` and `typer.Option` can create custom parameter types with a `parser` <abbr title="something that can be called like a function">callable</abbr>.

//// tab | Python 3.7+

```Python hl_lines="13-14  18-19"
{!> ../docs_src/parameter_types/custom_types/tutorial001_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="12-13  17-18"
{!> ../docs_src/parameter_types/custom_types/tutorial001.py!}
```

////

The function (or callable) that you pass to the parameter `parser` will receive the input value as a string and should return the parsed value with your own custom type.

## Click Custom Type

If you already have a <a href="https://click.palletsprojects.com/en/8.1.x/parameters/#implementing-custom-types" class="external-link" target="_blank">Click Custom Type</a>, you can use it in `typer.Argument()` and `typer.Option()` with the `click_type` parameter.

//// tab | Python 3.7+

```Python hl_lines="14-18  22-25"
{!> ../docs_src/parameter_types/custom_types/tutorial002_an.py!}
```

////
