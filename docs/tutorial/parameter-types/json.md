# JSON

To use JSON inputs use `dict` as Argument type

it will do something like

```python
import json

data = json.loads(user_input)
```

## Usage

You will get all the correct editor support, attributes, methods, etc for the dict object:

//// tab | Python 3.7+

```Python hl_lines="5"
{!> ../docs_src/parameter_types/json/tutorial001.py!}
```

////

Check it:

<div class="termy">

```console
// Run your program
$ python main.py --user-info '{"name": "Camila", "age": 15, "height_meters": 1.7, "female": true}'

User Info: {"name": "Camila", "age": 15, "height_meters": 1.7, "female": true}

```

</div>
