# Optional value for CLI Options

As in Click, providing a value to a *CLI option* can be made optional, in which case a default value will be used instead.

To make a *CLI option*'s value optional, you can annotate it as a *Union* of types *bool* and the parameter type.

/// info

You can create a type <a href="https://docs.python.org/3/library/typing.html#typing.Union" class="external-link" target="_blank">Union</a> by importing *Union* from the typing module.

For example `Union[bool, str]` represents a type that is either a boolean or a string.

You can also use the equivalent notation `bool | str`

///

Let's add a *CLI option* `--tone` with optional value:

{* docs_src/options/optional_value/tutorial001_an.py hl[5] *}

Now, there are three possible configurations:

* `--greeting` is not used, the parameter will receive a value of `False`.
```
python main.py
```

* `--greeting` is supplied with a value, the parameter will receive the string representation of that value.
```
python main.py --greeting <value>
```

* `--greeting` is used with no value, the parameter will receive the default `formal` value.
```
python main.py --greeting
```


And test it:

<div class="termy">

```console
$ python main.py Camila Gutiérrez

// We didn't pass the greeting CLI option, we get no greeting


// Now update it to pass the --greeting CLI option with default value
$ python main.py Camila Gutiérrez --greeting

Hello Camila Gutiérrez

// The above is equivalent to passing the --greeting CLI option with value `formal`
$ python main.py Camila Gutiérrez --greeting formal

Hi Camila !

// But you can select another value
$ python main.py Camila Gutiérrez --greeting casual

Hi Camila !
```

</div>
