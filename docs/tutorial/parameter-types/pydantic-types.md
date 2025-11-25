Pydantic types such as [AnyUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.AnyUrl) or [EmailStr](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.EmailStr) can be very convenient to describe and validate some parameters.

Pydantic is installed automatically when installing Typer with its extra standard dependencies:

<div class="termy">

```console
// Pydantic comes with typer
$ pip install typer
---> 100%
Successfully installed typer rich shellingham pydantic

// Alternatively, you can install Pydantic independently
$ pip install pydantic
---> 100%
Successfully installed pydantic

// Or if you want to use EmailStr
$ pip install "pydantic[email]"
---> 100%
Successfully installed pydantic, email-validator
```

</div>


You can then use them as parameter types.

{* docs_src/parameter_types/pydantic_types/tutorial001_an.py hl[9] *}

{* docs_src/parameter_types/pydantic_types/tutorial002_an.py hl[9] *}

These types are also supported in lists or tuples:

{* docs_src/parameter_types/pydantic_types/tutorial003_an.py hl[9] *}

{* docs_src/parameter_types/pydantic_types/tutorial004_an.py hl[9] *}
