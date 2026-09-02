# DateTime

You can specify a *CLI parameter* as a Python [`datetime`](https://docs.python.org/3/library/datetime.html).

Your function will receive a standard Python `datetime` object, and again, your editor will give you completion, etc.

{* docs_src/parameter_types/datetime/tutorial001_py310.py hl[1,9,10,11] *}

Typer will accept any string from datetime formats [supported by Pydantic](https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-9),
including Unix timestamps as seconds or milliseconds since the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time),
and several 'standard' options such as
* `%Y-%m-%d`
* `%Y-%m-%dT%H:%M:%S`
* `%Y-%m-%d %H:%M:%S`
* ...

Check it:

<div class="termy">

```console
$ uv run python main.py --help

Usage: main.py [OPTIONS] {birth}

Arguments:
  birth <datetime>  [required]

Options:
  --help                Show this message and exit.

// Pass a datetime
$ uv run python main.py 1956-01-31T10:00:00

Interesting day to be born: 1956-01-31 10:00:00
Birth hour: 10

// An invalid date
$ uv run python main.py july-19-1989

Usage: main.py [OPTIONS] {birth}
Try 'main.py --help' for help.

Error: Invalid value for 'birth': Input should be a valid datetime or date, invalid character in year
```

</div>

## Custom date format

You can also customize the formats received for the `datetime` with the `formats` parameter.

`formats` receives a list of strings with the date formats that would be passed to [datetime.strptime()](https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime).

For example, let's imagine that you want to accept an ISO formatted datetime, but for some strange reason, you also want to accept a format with:

* first the month
* then the day
* then the year
* separated with "`/`"

...It's a crazy example, but let's say you also needed that strange format:

{* docs_src/parameter_types/datetime/tutorial002_an_py310.py hl[13] *}

/// tip

Notice the last string in `formats`: `"%m/%d/%Y"`.

///

Check it:

<div class="termy">

```console
// ISO dates work (first pattern)
$ uv run python main.py 1969-10-29

Launch will be at: 1969-10-29 00:00:00

// The strange custom format also works (second pattern)
$ uv run python main.py 10/29/1969

Launch will be at: 1969-10-29 00:00:00

// But notice that a 'standard' date format now doesn't work anymore, as it's not included in 'formats':
$ uv run python main.py 1969-10-29T10:00:00

Usage: main.py [OPTIONS] {launch_date}
Try 'main.py --help' for help.

Error: Invalid value for 'launch_date': Value error, '1969-10-29T10:00:00' does not match the formats '%Y-%m-%d', '%m/%d/%Y'.

```

</div>
