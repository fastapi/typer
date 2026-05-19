# File objects

When you want to declare some types of files, you can use `Path`.
However, in some cases you may need to have access to a file-like object, and then you can use these [special File types](https://typer.tiangolo.com/tutorial/parameter-types/file/).

These objects can be imported from `typer` directly:

```python
from typer import FileBinaryRead, FileBinaryWrite, FileText, FileTextWrite
```

::: typer.FileText

::: typer.FileTextWrite

::: typer.FileBinaryRead

::: typer.FileBinaryWrite
