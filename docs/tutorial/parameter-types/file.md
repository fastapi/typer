Apart from `Path` *CLI parameters* you can also declare some types of "files".

!!! tip
    In most of the cases you are probably fine just using `Path`.

    You can read and write data with `Path` the same way.

The difference is that these types will give you a Python <a href="https://docs.python.org/3/glossary.html#term-file-object" class="external-link" target="_blank">file-like object</a> instead of a Python <a href="https://docs.python.org/3/library/pathlib.html#basic-use" class="external-link" target="_blank">Path</a>.

A "file-like object" is the same type of object returned by `open()` as in:

```Python
with open('file.txt') as f:
    # Here f is the file-like object
    read_data = f.read()
    print(read_data)
```

But in some special use cases you might want to use these special types. For example if you are migrating an existing application.

## `FileText` reading

`typer.FileText` gives you a file-like object for reading text, you will get `str` data from it.

This means that even if your file has text written in a non-english language, e.g. a `text.txt` file with:

```
la cigüeña trae al niño
```

You will have a `str` with the text inside, e.g.:

```Python
content = "la cigüeña trae al niño"
```

instead of having `bytes`, e.g.:

```Python
content = b"la cig\xc3\xbce\xc3\xb1a trae al ni\xc3\xb1o"
```

You will get all the correct editor support, attributes, methods, etc for the file-like object:

```Python hl_lines="4"
{!../docs_src/parameter_types/file/tutorial001.py!}
```

Check it:

<div class="termy">

```console
// Create a quick text config
$ echo "some settings" > config.txt

// Add another line to the config to test it
$ echo "some more settings" >> config.txt

// Now run your program
$ python main.py --config config.txt

Config line: some settings

Config line: some more settings
```

</div>

## `FileTextWrite`

For writing text, you can use `typer.FileTextWrite`:

```Python hl_lines="4 5"
{!../docs_src/parameter_types/file/tutorial002.py!}
```

This would be for writing human text, like:

```
some settings
la cigüeña trae al niño
```

...not to write binary `bytes`.

Check it:

<div class="termy">

```console
$ python main.py --config text.txt

Config written

// Check the contents of the file
$ cat text.txt

Some config written by the app
```

</div>

!!! info "Technical Details"
    `typer.FileTextWrite` is a just a convenience class.

    It's the same as using `typer.FileText` and setting `mode="w"`. You will learn about `mode` later below.

## `FileBinaryRead`

To read binary data you can use `typer.FileBinaryRead`.

You will receive `bytes` from it.

It's useful for reading binary files like images:

```Python hl_lines="4"
{!../docs_src/parameter_types/file/tutorial003.py!}
```

Check it:

<div class="termy">

```console
$ python main.py --file lena.jpg

Processed bytes total: 512
Processed bytes total: 1024
Processed bytes total: 1536
Processed bytes total: 2048
```

</div>

## `FileBinaryWrite`

To write binary data you can use `typer.FileBinaryWrite`.

You would write `bytes` to it.

It's useful for writing binary files like images.

Have in mind that you have to pass `bytes` to its `.write()` method, not `str`.

If you have a `str`, you have to encode it first to get `bytes`.

```Python hl_lines="4"
{!../docs_src/parameter_types/file/tutorial004.py!}
```

<div class="termy">

```console
$ python main.py --file binary.dat

Binary file written

// Check the binary file was created
$ ls ./binary.dat

./binary.dat
```

</div>

## File *CLI parameter* configurations

You can use several configuration parameters for these types (classes) in `typer.Option()` and `typer.Argument()`:

* `mode`: controls the "<a href="https://docs.python.org/3/library/functions.html#open" class="external-link" target="_blank">mode</a>" to open the file with.
    * It's automatically set for you by using the classes above.
    * Read more about it below.
* `encoding`: to force a specific encoding, e.g. `"utf-8"`.
* `lazy`: delay <abbr title="input and output, reading and writing files">I/O</abbr> operations. Automatic by default.
    * By default, when writing files, Click will generate a file-like object that is not yet the actual file. Once you start writing, it will go, open the file and start writing to it, but not before. This is mainly useful to avoid creating the file until you start writing to it. It's normally safe to leave this automatic. But you can overwrite it setting `lazy=False`. By default, it's `lazy=True` for writing and `lazy=False` for reading.
* `atomic`: if true, all writes will actually go to a temporal file and then moved to the final destination after completing. This is useful with files modified frequently by several users/programs.

## Advanced `mode`

By default, **Typer** will configure the <a href="https://docs.python.org/3/library/functions.html#open" class="external-link" target="_blank">`mode`</a> for you:

* `typer.FileText`: `mode="r"`, to read text.
* `typer.FileTextWrite`: `mode="w"`, to write text.
* `typer.FileBinaryRead`: `mode="rb"`, to read binary data.
* `typer.FileBinaryWrite`: `mode="wb"`, to write binary data.

### Note about `FileTextWrite`

`typer.FileTextWrite` is actually just a convenience class. It's the same as using `typer.FileText` with `mode="w"`.

But it's probably shorter and more intuitive as you can get it with autocompletion in your editor by just starting to type `typer.File`... just like the other classes.

### Customize `mode`

You can override the `mode` from the defaults above.

For example, you could use `mode="a"` to write "appending" to the same file:

```Python hl_lines="4"
{!../docs_src/parameter_types/file/tutorial005.py!}
```

!!! tip
    As you are manually setting `mode="a"`, you can use `typer.FileText` or `typer.FileTextWrite`, both will work.

Check it:

<div class="termy">

```console
$ python main.py --config config.txt

Config line written

// Run your program a couple more times to see how it appends instead of overwriting
$ python main.py --config config.txt

Config line written

$ python main.py --config config.txt

Config line written

// Check the contents of the file, it should have each of the 3 lines appended
$ cat config.txt

This is a single line
This is a single line
This is a single line
```

</div>

## About the different types

!!! info
    These are technical details about why the different types/classes provided by **Typer**.

    But you don't need this information to be able to use them. You can skip it.

**Typer** provides you these different types (classes) because they inherit directly from the actual Python implementation that will be provided underneath for each case.

This way your editor will give you the right type checks and completion for each type.

Even if you use `lazy`. When you use `lazy` Click creates a especial object to delay writes, and serves as a "proxy" to the actual file that will be written. But this especial proxy object doesn't expose the attributes and methods needed for type checks and completion in the editor. If you access those attributes or call the methods, the "proxy" lazy object will call them in the final object and it will all work. But you wouldn't get autocompletion for them.

But because these **Typer** classes inherit from the actual implementation that will be provided underneath (not the lazy object), you will get all the autocompletion and type checks in the editor.
