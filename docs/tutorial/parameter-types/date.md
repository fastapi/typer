You can specify a *CLI parameter* as a Python <a href="https://docs.python.org/3/library/datetime.html" class="external-link" target="_blank">`date`</a>.

Your function will receive a standard Python `date` object, and again, your editor will give you completion, etc.

```Python hl_lines="2  7 8 9"
{!../docs_src/parameter_types/date/tutorial001.py!}
```

Typer will accept any string from the following formats:

* `%Y-%m-%d`

Check it:

<div class="termy">

```console
$ python main.py --help

Usage: main.py [OPTIONS] BIRTH:[%Y-%m-%d]

Arguments:
  BIRTH:[%Y-%m-%d][required]

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or customize the installation.
  --help                Show this message and exit.

// Pass a date
$ python main.py 1956-01-31

Interesting day to be born: 1956-01-31
Birth week name: Tuesday

// An invalid date
$ python main.py july-19-1989

Usage: main.py [OPTIONS] BIRTH:[%Y-%m-%d]

Error: Invalid value for 'BIRTH:[%Y-%m-%d]': 'july-19-1989' does not match the format '%Y-%m-%d'.
```

</div>

## Custom date format

You can also customize the formats received for the `date` with the `formats` parameter.

`formats` receives a list of strings with the date formats that would be passed to <a href="https://docs.python.org/3/library/datetime.html#datetime.date.strftime" class="external-link" target="_blank">datetime.strptime()</a>.

For example, let's imagine that you want to accept an ISO formatted date, but for some strange reason, you also want to accept a format with:

* first the month
* then the day
* then the year
* separated with "`/`"

...It's a crazy example, but let's say you also needed that strange format:

```Python hl_lines="8"
{!../docs_src/parameter_types/date/tutorial002.py!}
```

!!! tip
    Notice the last string in `formats`: `"%m/%d/%Y"`.

Check it:

<div class="termy">

```console
// ISO dates work
$ python main.py 1969-10-29

Launch will be at: 1969-10-29

// But the strange custom format also works
$ python main.py 10/29/1969

Launch will be at: 1969-10-29
```

</div>
