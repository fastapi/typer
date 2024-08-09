# Launching Applications

You can launch applications from your CLI program with `typer.launch()`.

It will launch the appropriate application depending on the URL or file type you pass it:

```Python hl_lines="6"
{!../docs_src/launch/tutorial001.py!}
```

Check it:

<div class="termy">

```console
$ python main.py

Opening Typer docs

// Opens browser with Typer's docs
```

</div>

## Locating a file

You can also make the operating system open the file browser indicating where a file is located with `locate=True`:

```Python hl_lines="17"
{!../docs_src/launch/tutorial002.py!}
```

/// tip

The rest of the code in this example is just making sure the app directory exists and creating the config file.

But the most important part is the `typer.launch(config_file_str, locate=True)` with the argument `locate=True`.

///

Check it:

<div class="termy">

```console
$ python main.py

Opening config directory

// Opens a file browser indicating where the config file is located
```

</div>
