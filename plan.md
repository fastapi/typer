# Args and Kwargs support

This PR adds support for `*args` and `**kwargs` in function signatures:

```python
# -- command.py --

import json
from typing import Any

import typer

@app.command()
def cmd(
    filepath: Path,
    option: str = "",
    flag: bool = False,
    *args: str,
    **kwargs: Any
) -> None:
    dump = json.dumps({
        "filepath" : filepath,
        "option" : option,
        "flag" : flag,
        "args" : args,
        "kwargs" : kwargs,

    })
    typer.echo(dump)
```

Declaring a signature allows passing arbitrary key-value pairs on the command line,
which are then made available in `kwargs`. Unknown trailing arguments are captured in `*args`.

```bash
./command.py --unknown-key value input.txt arg1 arg2
# kwargs = { "unknown_key" : "value" }; args = ( "arg1", "arg2" )
```

To avoid ambiguity, everything after `--` will be absorbed into `*args` regardless of
whether or not it matches a known argument. (This is a widely used convention. See e.g. XX.)

```bash
./command.py input.txt --flag # flag = True
./command.py input.txt -- --flag # args = ("--flag",)

./command.py input.txt arg1 --unknown option # args = ( "arg1" ); kwargs = { "unknown" : "option" }
./command.py input.txt -- arg1 --unknown option # args = ( "arg1", "--unknown", "option" )
```

This feature will not disrupt explicitly declared flags/options.

```bash
# all of the following commands are parsed equivalently:
# option = "val"; flag = True; args = ( "arg1", "arg2" ); kwargs = { "unknown", "val2" }

./command.py --option val --flag --unknown val2 input.txt arg1 arg2
./command.py --flag --unknown val2 input.txt --option val arg1 arg2
./command.py --flag input.txt --option val --unknown val2 arg1 arg2
./command.py --flag input.txt --option val --unknown val2 -- arg1 arg2
```

Empty args are handled gracefully.

```bash
# both of the following produce args = ()
./command.py input.txt
./command.py input.txt --
```

Unknown options *must* have values.
(To emulate a boolean flag, simply pass a value so that `kwargs.get("unknown_flag")` is truthy.)

```bash
./command.py --unknown-flag input.txt arg1 arg2 # not okay
./command.py --unknown-flag true input.txt arg1 arg2 # okay
```

Both `*args` and `**kwargs` can of course be declared without the other.

```python
# -- command2.py --

from typing import Any

import typer


@app.command()
def args(filepath: Path, *args: str) -> None:
    typer.echo(args)

@app.command()
def kwargs(filepath: Path, **kwargs: Any) -> None:
    typer.echo(kwargs)
```

```bash
./command2.py args input.txt arg1 arg2 # args = ( "arg1", "arg2" )
./command2.py kwargs input.txt --key value # kwargs = { "key": "value" }
```

Closes #XX.

## Potential TODO items

- Allow `=` to declare kwargs, for example `./command --unknown=value input.txt`
