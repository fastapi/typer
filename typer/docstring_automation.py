"""Docstring parser for the following styles:

- Numpy https://numpydoc.readthedocs.io/en/latest/format.html
- Google https://google.github.io/styleguide/pyguide.html#381-docstrings
- Sphinx https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html

"""

import inspect
from typing import Any, Callable, List, Tuple, Union

import click

NUMPY = "NUMPY"
GOOGLE = "GOOGLE"
SPHINX = "SPHINX"
NUMPY_PARAMS = "Parameters"
GOOGLE_PARAMS = "Args:"
SPHINX_PARAM = ":param"
SPHINX_RETURNS = ":returns"
SPHINX_RAISES = ":raises"
DOCSTRING_SECTIONS = {
    NUMPY_PARAMS: True,
    "Returns": True,
    "Yields": True,
    "Receives": True,
    "Raises": True,
    "Warns": True,
    "Warnings": True,
    "See Also": True,
    "References": True,
    "Notes": True,
    "Examples": True,
    "Attributes": True,
    "Methods": True,
    GOOGLE_PARAMS: True,
    "Returns:": True,
    "Yields:": True,
    "Raises:": True,
    "Attributes:": True,
}
DOCSTRING_STYLES_PARAMS = {
    NUMPY: NUMPY_PARAMS,
    GOOGLE: GOOGLE_PARAMS,
}


def get_help_from_docstring(command: Callable[..., Any]) -> str:
    """
    Get help message from callable object.

    Parameters
    ----------
    command : Callable[..., Any]
        Callable object (command, callback, ...).

    Returns
    -------
    str
        Docstring summary, if exists.

    """
    docstring = inspect.getdoc(command)
    if not docstring:
        return ""
    docstring_lines = docstring.strip().splitlines()
    help_message = ""
    for line in docstring_lines:
        if DOCSTRING_SECTIONS.get(line.strip()) or line.strip().startswith(
            (SPHINX_PARAM, SPHINX_RETURNS, SPHINX_RAISES)
        ):
            break
        help_message += line + "\n" if line else ""
    return help_message


def get_index_of_sphinx_param_section(
    docstring_lines: List[str],
) -> Tuple[int, str]:
    """
    Get list index of Sphinx parameters section in docstring lines.

    Parameters
    ----------
    docstring_lines : List[str]
        Lines of the docstring.

    Returns
    -------
    Tuple[int, str]
        Index and docstring style.

    """
    index_param_section = 0
    docstring_style = ""
    for index, line in enumerate(docstring_lines):
        if line.strip().startswith(SPHINX_PARAM):
            index_param_section = index - 1
            docstring_style = SPHINX
            break
    return index_param_section, docstring_style


def get_param_help_from_numpy_docstring(
    docstring_lines: List[str], index_param_section: int, param_name: str
) -> str:
    """
    Get parameter help message from Numpy style docstring.

    Parameters
    ----------
    docstring_lines : List[str]
        Lines of the docstring.
    index_param_section : int
        List index of the parameters section in the lines of the docstring.
    param_name : str
        Name of the parameter.

    Returns
    -------
    str
        Parameter help message, if any.

    """
    index_param_section += 1
    help_message = ""
    for index, line in enumerate(docstring_lines[index_param_section:]):
        if line.strip().startswith(param_name):
            help_message = docstring_lines[index + index_param_section + 1]
            help_message = help_message.split(", by default")[0]
            if help_message[-1] != ".":
                help_message += "."
            break
    return help_message.strip()


def get_param_help_from_google_docstring(
    docstring_lines: List[str], index_param_section: int, param_name: str
) -> str:
    """
    Get parameter help message from Google style docstring.

    Parameters
    ----------
    docstring_lines : List[str]
        Lines of the docstring.
    index_param_section : int
        List index of the parameters section in the lines of the docstring.
    param_name : str
        Name of the parameter.

    Returns
    -------
    str
        Parameter help message, if any.

    """
    help_message = ""
    for index, line in enumerate(docstring_lines[index_param_section:]):
        if line.strip().startswith(param_name):
            help_message = docstring_lines[index + index_param_section]
            help_message = help_message.split(":", maxsplit=2)[1]
            help_message = help_message.split(" Defaults to", maxsplit=2)[0]
            if help_message[-1] != ".":
                help_message += "."
            break
    return help_message.strip()


def get_param_help_from_sphinx_docstring(
    docstring_lines: List[str], index_param_section: int, param_name: str
) -> str:
    """
    Get parameter help message from Sphinx style docstring.

    Parameters
    ----------
    docstring_lines : List[str]
        Lines of the docstring.
    index_param_section : int
        List index of the parameters section in the lines of the docstring.
    param_name : str
        Name of the parameter.

    Returns
    -------
    str
        Parameter help message, if any.

    """
    help_message = ""
    for index, line in enumerate(docstring_lines[index_param_section:]):
        if line.strip().startswith(f"{SPHINX_PARAM} {param_name}"):
            help_message = docstring_lines[index + index_param_section]
            help_message = help_message.split(":", maxsplit=3)[2]
            help_message = help_message.split(", defaults to", maxsplit=2)[0]
            if help_message[-1] != ".":
                help_message += "."
            break
    return help_message.strip()


def get_param_help_from_docstring(
    param: Union[click.Argument, click.Option], command: Callable[..., Any]
) -> str:
    """
    Get parameter help message from from callable object's docstring.

    Parameters
    ----------
    param : Union[click.Argument, click.Option]
        Parameter of the command.
    command : Callable[..., Any]
        Callable object (command, callback, ...).

    Returns
    -------
    str
        Parameter help message, if any.

    """
    docstring = inspect.getdoc(command)
    if not docstring:
        return ""
    docstring_lines = docstring.strip().splitlines()
    index_param_section = 0
    docstring_style = ""
    for style, param_section in DOCSTRING_STYLES_PARAMS.items():
        try:
            index_param_section = docstring_lines.index(param_section)
            if index_param_section:
                docstring_style = style
                break
        except ValueError:
            continue
    if not docstring_style:
        (
            index_param_section,
            docstring_style,
        ) = get_index_of_sphinx_param_section(docstring_lines)
    if not docstring_style:
        return ""

    get_help_message = {
        NUMPY: get_param_help_from_numpy_docstring,
        GOOGLE: get_param_help_from_google_docstring,
        SPHINX: get_param_help_from_sphinx_docstring,
    }
    return get_help_message[docstring_style](
        docstring_lines=docstring_lines,
        index_param_section=index_param_section,
        param_name=param.name,  # type: ignore
    )
