Typer allows you to use [async](https://docs.python.org/3/library/asyncio.html) functions.

```Python
{!../docs_src/async_cmd/async001.py!}
```

<div class="termy">

```console
$ python main.py

Hello Async World
```

</div>

It also works with commands, and you can mix regular and async commands:

```Python
{!../docs_src/async_cmd/async002.py!}
```

<div class="termy">

```console
$ python main.py sync

Hello Sync World

$ python main.py async

Hello Async World
```
</div>

!!! info
    Under the hood, Typer is running your async functions with [asyncio.run()](https://docs.python.org/3/library/asyncio-runner.html#asyncio.run)

!!! warning
    Typer only supports async functions on Python 3.7+
