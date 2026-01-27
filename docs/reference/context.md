# Context

When you create a Typer application it uses Click underneath.
And every Click application has a special object called a [`Context`](https://click.palletsprojects.com/en/stable/api/#click.Context) that is normally hidden.
But you can access the context by declaring a function parameter of type `typer.Context`.

The same way you can access the context by declaring a function parameter with its value,
you can declare another function parameter with type `typer.CallbackParam` to get the specific Click [`Parameter`](https://click.palletsprojects.com/en/stable/api/#click.Parameter) object.

```python
from typing import Annotated

import typer

app = typer.Typer()


def name_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if ctx.resilient_parsing:
        return
    print(f"Validating param: {param.name}")
    if value != "Rick":
        raise typer.BadParameter("Only Rick is allowed")
    return value


@app.command()
def main(name: Annotated[str | None, typer.Option(callback=name_callback)] = None):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
```

::: typer.Context

::: typer.CallbackParam
