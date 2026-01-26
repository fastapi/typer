# File objects

These objects can be imported from `typer` directly:

```python
from typer import FileBinaryRead, FileBinaryWrite, FileText, FileTextWrite
```

When you want to declare some types of files, you can use `Path`. 
However, in some cases you may need to have access to a file-like object, and then you can use these [special types](https://typer.tiangolo.com/tutorial/parameter-types/file/).

::: typer.FileText

::: typer.FileTextWrite

::: typer.FileBinaryRead

::: typer.FileBinaryWrite