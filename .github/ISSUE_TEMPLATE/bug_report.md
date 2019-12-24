---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

### Describe the bug

Write here a clear and concise description of what the bug is.

### To Reproduce

Steps to reproduce the behavior with a minimum self-contained file.

Replace each part with your own scenario:

* Create a file `main.py` with:

```Python
import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


if __name__ == "__main__":
    app()
```

* Call it with:

```bash
python main.py Camila
```

* It outputs:

```
Hello Camila
```

* But I expected it to output:

```
Hello World
```

### Expected behavior

Add a clear and concise description of what you expected to happen.

### Screenshots

If applicable, add screenshots to help explain your problem.

### Environment

* OS: [e.g. Linux / Windows / macOS]
* Typer Version [e.g. 0.3.0], get it with:

```bash
python -c "import typer; print(typer.__version__)"
```

* Python version, get it with:

```bash
python --version
```

### Additional context

Add any other context about the problem here.
