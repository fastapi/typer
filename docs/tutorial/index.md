# Learn

Learn how to use **Typer** in this step-by-step **Tutorial** - **User Guide**.

It covers everything you need to know from the **simplest scripts** to **complex CLI applications**.

You could consider this a **book**, a **course**, the **official** and recommended way to learn **Typer**. 😎

## Python Types

If you need a refresher about how to use Python type hints, check the first part of <a href="https://fastapi.tiangolo.com/python-types/" class="external-link" target="_blank">FastAPI's Python types intro</a>.

You can also check the <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">mypy cheat sheet</a>.

In short (very short), you can declare a function with parameters like:

```Python
from typing import Optional

def type_example(name: str, formal: bool = False, intro: Optional[str] = None):
    pass
```

And your editor (and **Typer**) will know that:

* `name` is of type `str` and is a required parameter.
* `formal` is a `bool` and is by default `False`.
* `intro` is an optional `str`, by default is `None`.

These type hints are what give you autocomplete in your editor and several other features.

**Typer** is based on these type hints.

## About this Tutorial

This tutorial shows you how to use **Typer** with all its features, step by step.

Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific CLI needs.

It is also built to work as a future reference so you can come back and see exactly what you need.

## Run the Code

All the code blocks can be copied and used directly (they are tested Python files).

To run any of the examples, copy the code to a file `main.py`, and run it:

<div class="termy">

```console
$ python main.py

✨ The magic happens here ✨
```

</div>

It is **HIGHLY encouraged** that you write or copy the code, edit it and run it locally.

Using it in your editor is what really shows you the benefits of **Typer**, seeing how little code you have to write, all the **inline errors**, **autocompletion**, etc.

And running the examples is what will really help you **understand** what is going on.

You can learn a lot more by **running some examples** and **playing around** with them than by reading all the docs here.
