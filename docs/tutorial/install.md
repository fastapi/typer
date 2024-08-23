# Install **Typer**

The first step is to install **Typer**.

First, make sure you create your [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install it, for example with:

<div class="termy">

```console
$ pip install typer
---> 100%
Successfully installed typer click shellingham rich
```

</div>

By default, `typer` comes with `rich` and `shellingham`.

/// note

If you are an advanced user and want to opt out of these default extra dependencies, you can instead install `typer-slim`.

```bash
pip install typer
```

...includes the same optional dependencies as:

```bash
pip install "typer-slim[standard]"
```

///
