from typing import Optional

import typer


def function_to_test_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """Used by docstring automation tests."""


SUMMARY = "Function to test docstring styles."
PARAMS = {
    "param1": "A very detailed description.",
    "param2": "A small one.",
    "param3": "A description with default value.",
}
DOCSTRINGS = {
    "NUMPY": """
    Function to test docstring styles.

    Parameters
    ----------
    param1 : str
        A very detailed description.
    param2 : int
        A small one
    param3 : Optional[str], optional
        A description with default value, by default None

    Returns
    -------
    str
        Return information.

    """,
    "GOOGLE": """
    Function to test docstring styles.

    Args:
        param1 (str): A very detailed description.
        param2 (int): A small one
        param3 (Optional[str], optional): A description with default value.
            Defaults to None.

    Returns:
        str: Return information.

    """,
    "SPHINX": """
    Function to test docstring styles.

    :param param1: A very detailed description.
    :type param1: str
    :param param2: A small one
    :type param2: int
    :param param3: A description with default value, defaults to None
    :type param3: Optional[str], optional
    :return: Return information.
    :rtype: str

    """,
}

PRIORITY_SUMMARY = "Not automated!"
PRIORITY_PARAM_DOC = "A complete different one."


def function_to_test_priority(
    param1: str = typer.Argument(...),
    param2: int = typer.Argument(..., help=PRIORITY_PARAM_DOC),
    param3: Optional[str] = None,
) -> str:
    """Used to test if docstring automation respects priority."""
