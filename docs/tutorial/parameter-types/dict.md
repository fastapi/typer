# Dict

You can declare a *CLI parameter* to be a standard Python `dict`:

{* docs_src/parameter_types/dict/tutorial001_an.py hl[5] *}

Check it:

<div class="termy">

```console
// Run your program
$ python main.py --user-info '{"name": "Camila", "age": 15, "height": 1.7, "female": true}'

Name: Camila
User attributes: ['age', 'female', 'height', 'name']

```

</div>

This can be particularly useful when you want to include JSON input:

```python
import json

data = json.loads(user_input)
```
