# Parameters

Parameters to our command line interface may be both [options](https://typer.tiangolo.com/tutorial/options/) and [arguments](https://typer.tiangolo.com/tutorial/arguments/):

```python
from typing import Annotated
import typer

app = typer.Typer()


@app.command()
def main(
    id: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"ID is {id}")
    print(f"--age is {age}")
    print(f"--score is {score}")
```

::: typer.Argument
    options:
      show_overloads: false

::: typer.Option
    options:
      show_overloads: false


