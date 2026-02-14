# Custom Types

You can easily use your own custom types in your **Typer** applications.

The way to do it is by providing a way to <abbr title="convert from some plain format, like the input text in the CLI, into Python objects">parse</abbr> input into your own types.

## Type Parser

`typer.Argument` and `typer.Option` can create custom parameter types with a `parser` <abbr title="something that can be called like a function">callable</abbr>.

{* docs_src/parameter_types/custom_types/tutorial001_an_py39.py hl[14:15,23:24] *}

The function (or callable) that you pass to the parameter `parser` will receive the input value as a string and should return the parsed value with your own custom type.
