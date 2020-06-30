You can declare a *CLI parameter* to be a standard Python <a href="https://docs.python.org/3/library/pathlib.html#basic-use" class="external-link" target="_blank">`pathlib.Path`</a>.

This is what you would do for directory paths, file paths, etc:

```Python hl_lines="1  7"
{!../docs_src/parameter_types/path/tutorial001.py!}
```

And again, as you receive a standard Python `Path` object the same as the type annotation, your editor will give you autocompletion for all its attributes and methods.

Check it:

<div class="termy">

```console
// No config
$ python main.py

No config file
Aborted!

// Pass a config that doesn't exist
$ python main.py --config config.txt

The config doesn't exist

// Now create a quick config
$ echo "some settings" > config.txt

// And try again
$ python main.py --config config.txt

Config file contents: some settings

// And with a directory
$ python main.py --config ./

Config is a directory, will use all its config files
```

</div>

## Path validations

You can perform several validations for `Path` *CLI parameters*:

* `exists`: if set to true, the file or directory needs to exist for this value to be valid. If this is not required and a file does indeed not exist, then all further checks are silently skipped.
* `file_okay`: controls if a file is a possible value.
* `dir_okay`: controls if a directory is a possible value.
* `writable`: if true, a writable check is performed.
* `readable`: if true, a readable check is performed.
* `resolve_path`: if this is true, then the path is fully resolved before the value is passed onwards. This means that it’s absolute and <abbr title="symbolic links, also known as shortcuts. Links in a file system that point to other location. For example, some applications when installed create symlinks in the desktop to launch them.">symlinks</abbr> are resolved.

!!! note "Technical Details"
    It will not expand a tilde-prefix (something with `~`, like `~/Documents/`), as this is supposed to be done by the shell only.

!!! tip
    All these parameters come directly from <a href="https://click.palletsprojects.com/en/7.x/parameters/#parameter-types" class="external-link" target="_blank">Click</a>.

For example:

```Python hl_lines="9 10 11 12 13 14"
{!../docs_src/parameter_types/path/tutorial002.py!}
```

Check it:

<div class="termy">

```console
$ python main.py --config config.txt

Usage: main.py [OPTIONS]
Try "main.py --help" for help.

Error: Invalid value for '--config': File 'config.txt' does not exist.

// Now create a quick config
$ echo "some settings" > config.txt

// And try again
$ python main.py --config config.txt

Config file contents: some settings

// And with a directory
$ python main.py --config ./

Usage: main.py [OPTIONS]
Try "main.py --help" for help.

Error: Invalid value for '--config': File './' is a directory.
```

</div>

### Advanced `Path` configurations

!!! warning "Advanced Details"
    You probably won't need these configurations at first, you may want to skip it.

    They are used for more advanced use cases.

* `allow_dash`: If this is set to True, a single dash to indicate standard streams is permitted.
* `path_type`: optionally a string type that should be used to represent the path. The default is None which means the return value will be either bytes or unicode depending on what makes most sense given the input data Click deals with.
