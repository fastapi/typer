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

```Python
{!../docs_src/asynchronous/tutorial001.py!}
```

Or using `anyio`:

```Python
{!../docs_src/asynchronous/tutorial002.py!}
```

<small>Important to note, `typer.run()` doesn't provide means to customize the async run behavior.</small>

## Using with commands

Async functions can be registered as commands just like synchronous functions:

```Python
{!../docs_src/asynchronous/tutorial003.py!}
```

Or using `anyio`:

```Python
{!../docs_src/asynchronous/tutorial004.py!}
```

Or using `trio` via `anyio`:

```Python
{!../docs_src/asynchronous/tutorial005.py!}
```

## Using with callback

The callback function supports asynchronous functions just like commands including the `async_runner` parameter:

```Python
{!../docs_src/asynchronous/tutorial006.py!}
```

Because the asynchronous functions are wrapped in a synchronous context before being executed, it is possible to mix async engines between the callback and commands.

## Customizing async engine

Customizing the used async engine is as simple a providing an additional parameter to the Typer instance or the decorators.

The `async_runner` provided to the decorator always overwrites the typer instances `async_runner`.

Customize a single command:

```Python
{!../docs_src/asynchronous/tutorial007.py!}
```

Customize the default engine for the Typer instance:

```Python
{!../docs_src/asynchronous/tutorial008.py!}
```
