# Async support

## Engines

Typer supports `asyncio` out of the box. <a href="https://github.com/python-trio/trio" class="external-link" target="_blank"><code>Trio</code></a> is supported through
<a href="https://github.com/agronholm/anyio" class="external-link" target="_blank"><code>anyio</code></a>, which can be installed as optional dependency:

<div class="termy">

```console
$ pip install typer[anyio]
---> 100%
Successfully installed typer anyio
```

</div>

### Default engine selection

*none* | anyio | trio | anyio + trio
--- | --- | --- | ---
asyncio | asyncio via anyio | asyncio* | trio via anyio

<small>* If you don't want to install `anyio` when using `trio`, provide your own async_runner function</small>

## Using with run()

Async functions can be run just like normal functions:

{* docs_src/asynchronous/tutorial001.py hl[1,8:9,14] *}

Or using `anyio`:

{* docs_src/asynchronous/tutorial002.py hl[1,8] *}

## Using with commands

Async functions can be registered as commands explicitely just like synchronous functions:

{* docs_src/asynchronous/tutorial003.py hl[1,8:9,15] *}

Or using `anyio`:

{* docs_src/asynchronous/tutorial004.py hl[1,9] *}

Or using `trio` via `anyio`:

{* docs_src/asynchronous/tutorial005.py hl[1,9] *}

## Customizing async engine

You can customize the async engine by providing an additional parameter `async_runner` to the Typer instance or to the command decorator.

When both are provided, the one from the decorator will take precedence over the one from the Typer instance.

Customize a single command:

{* docs_src/asynchronous/tutorial007.py hl[15] *}

Customize the default engine for the Typer instance:

{* docs_src/asynchronous/tutorial008.py hl[6] *}

## Using with callback

The callback function supports asynchronous functions with the `async_runner` parameter as well:

{* docs_src/asynchronous/tutorial006.py hl[15] *}

Because the asynchronous functions are wrapped in a synchronous context before being executed, it is possible to mix async engines between the callback and commands.
