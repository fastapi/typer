# Parameters

Parameters to our command line interface may be both [CLI Options](https://typer.tiangolo.com/tutorial/options/) and [CLI Arguments](https://typer.tiangolo.com/tutorial/arguments/):

```python
from typing import Annotated
import typer

app = typer.Typer()

@app.command()
def register(
    user: Annotated[str, typer.Argument()],
    age: Annotated[int, typer.Option(min=18)],
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"User is {user}")
    print(f"--age is {age}")
    print(f"--score is {score}")

if __name__ == "__main__":
    app()
```

::: typer.Argument
    options:
      show_overloads: false

::: typer.Option
    options:
      show_overloads: false
