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

=== "Python 3.7+ Argument"

    ```Python hl_lines="5"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial001_an.py!}
    ```

=== "Python 3.7+ Argument non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="4"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial001.py!}
    ```

=== "Python 3.7+ Option"

    ```Python hl_lines="5"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial002_an.py!}
    ```

=== "Python 3.7+ Option non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="4"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial002.py!}
    ```

These types are also supported in lists or tuples

=== "Python 3.7+ list"

    ```Python hl_lines="6"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial003_an.py!}
    ```

=== "Python 3.7+ list non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="5"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial003.py!}
    ```

=== "Python 3.7+ tuple"

    ```Python hl_lines="6"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial004_an.py!}
    ```

=== "Python 3.7+ tuple non-Annotated"

    !!! tip
        Prefer to use the `Annotated` version if possible.

    ```Python hl_lines="5"
    {!> ../docs_src/parameter_types/pydantic_types/tutorial004.py!}
    ```
