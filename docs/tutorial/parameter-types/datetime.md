# DateTime

You can specify a *CLI parameter* as a Python <a href="https://docs.python.org/3/library/datetime.html" class="external-link" target="_blank">`datetime`</a>.

Your function will receive a standard Python `datetime` object, and again, your editor will give you completion, etc.

```Python hl_lines="1  6 7 8"
{!../docs_src/parameter_types/datetime/tutorial001.py!}
```

Typer will accept any string from the following formats:

* `%Y-%m-%d`
* `%Y-%m-%dT%H:%M:%S`
* `%Y-%m-%d %H:%M:%S`

Check it:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]

Arguments:
  BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S][required]

Options:
  --help                Show this message and exit.

// Pass a datetime
$ python main.py 1956-01-31T10:00:00

Interesting day to be born: 1956-01-31 10:00:00
Birth hour: 10

// An invalid date
$ python main.py july-19-1989

Usage: main.py [OPTIONS] [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d%H:%M:%S]

Error: Invalid value for 'BIRTH:[%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]': 'july-19-1989' does not match the formats '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'.
```

</div>

## Custom date format

You can also customize the formats received for the `datetime` with the `formats` parameter.

`formats` receives a list of strings with the date formats that would be passed to <a href="https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime" class="external-link" target="_blank">datetime.strptime()</a>.

For example, let's imagine that you want to accept an ISO formatted datetime, but for some strange reason, you also want to accept a format with:

* first the month
* then the day
* then the year
* separated with "`/`"

...It's a crazy example, but let's say you also needed that strange format:

//// tab | Python 3.7+

```Python hl_lines="11"
{!> ../docs_src/parameter_types/datetime/tutorial002_an.py!}
```

////

//// tab | Python 3.7+ non-Annotated

/// tip

Prefer to use the `Annotated` version if possible.

///

```Python hl_lines="8"
{!> ../docs_src/parameter_types/datetime/tutorial002.py!}
```

////

/// tip

Notice the last string in `formats`: `"%m/%d/%Y"`.

///

Check it:

<div class="termy">

```console
// ISO dates work
$ python main.py 1969-10-29

Launch will be at: 1969-10-29 00:00:00

// But the strange custom format also works
$ python main.py 10/29/1969

Launch will be at: 1969-10-29 00:00:00
```

</div>
