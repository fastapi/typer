# Context

Every app has a special internal object that keeps track of state relevant to the script's execution.
For some advanced use-cases, you may want to access it directly.
This can be done by declaring a function parameter of type `typer.Context`.

Similarly, you can also declare a function parameter with type `typer.CallbackParam` in case a callback could be used
by several CLI parameters, and you need to figure out which one it was.


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
