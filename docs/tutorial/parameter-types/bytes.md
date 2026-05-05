# Bytes

You can declare `bytes` for CLI arguments and options.

By default, `bytes` are created by encoding the input string with UTF-8 (the same as Python's default for `str.encode()`), but you can configure the encoding and error handling.

## Default UTF-8 encoding

This example declares a `bytes` argument using the default UTF-8 encoding:

{* docs_src/parameter_types/bytes/tutorial001.py hl[7:9] *}

Try it with non-ASCII characters and you will get UTF-8 encoded bytes.

## Custom encoding on Argument

You can set a specific encoding for a `bytes` argument:

{* docs_src/parameter_types/bytes/tutorial002.py hl[7] *}

Here the argument is configured with `encoding="latin-1"`, so the command line input will be encoded accordingly.

## Custom encoding and errors on Option

You can also configure a `bytes` option with a specific encoding and error handling mode:

{* docs_src/parameter_types/bytes/tutorial003.py hl[7] *}

The `errors` parameter supports the same values as Python's `str.encode()` (e.g. `"strict"`, `"ignore"`, `"replace"`).

## Primary use case

The goal of supporting `bytes` is to let you write a single function that works both:

- Inside Typer: when called as a CLI, Typer parses command line input and converts it to `bytes` using the configured `encoding`/`errors`.
- Outside Typer: when called as regular Python code, you can pass `bytes` directly, without any CLI parsing involved.

This keeps your function reusable in both contexts while giving you control over how CLI text inputs are converted to `bytes`.
