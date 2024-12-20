from gettext import gettext
from typing import Any, Optional

from rich.box import HEAVY_HEAD
from rich.table import Table

DEFAULT_ROW_PROPS = {
    "justify": "left",
    "no_wrap": True,
    "overflow": "ignore",
}

# allow for i18n/l8n
ITEMS = gettext("Items")
PROPERTY = gettext("Property")
PROPERTIES = gettext("Properties")
VALUE = gettext("Value")
VALUES = gettext("Values")
UNKNOWN = gettext("Unknown")
FOUND_ITEMS = gettext("Found {} items")
ELLIPSIS = gettext("...")

OBJECT_HEADERS = [PROPERTY, VALUE]

KEY_FIELDS = ["name", "id"]
URL_PREFIXES = ["http://", "https://", "ftp://"]

KEY_MAX_LEN = 35
VALUE_MAX_LEN = 50
URL_MAX_LEN = 100


# NOTE: the key field of dictionaries are expected to be be `str`, `int`, `float`, but use
#       `Any` readability.


class RichTable(Table):
    """
    This is wrapper around the rich.Table to provide some methods for adding complex items.
    """

    def __init__(
        self,
        *args: Any,
        outer: bool = True,
        row_props: dict[str, Any] = DEFAULT_ROW_PROPS,
        **kwargs: Any,
    ):
        super().__init__(
            # items with "regular" defaults
            highlight=kwargs.pop("highlight", True),
            row_styles=kwargs.pop("row_styles", None),
            expand=kwargs.pop("expand", False),
            caption_justify=kwargs.pop("caption_justify", "left"),
            border_style=kwargs.pop("border_style", None),
            leading=kwargs.pop(
                "leading", 0
            ),  # warning: setting to non-zero disables lines
            # these items take queues from `outer`
            show_header=kwargs.pop("show_header", outer),
            show_edge=kwargs.pop("show_edge", outer),
            box=HEAVY_HEAD if outer else None,
            **kwargs,
        )
        for name in args:
            self.add_column(name, **row_props)


def _truncate(s: str, max_length: int) -> str:
    """Truncates the provided string to a maximum of max_length (including elipsis)"""
    if len(s) < max_length:
        return s
    return s[: max_length - 3] + ELLIPSIS


def _get_name_key(item: dict[Any, Any]) -> Optional[str]:
    """Attempts to find an identifying value."""
    for k in KEY_FIELDS:
        key = str(k)
        if key in item:
            return key

    return None


def _is_url(s: str) -> bool:
    """Rudimentary check for somethingt starting with URL prefix"""
    return any(s.startswith(p) for p in URL_PREFIXES)


def _create_list_table(items: list[dict[Any, Any]], outer: bool) -> RichTable:
    """Creates a table from a list of dictionary items.

    If an identifying "name key" is found (in the first entry), the table will have 2 columns: name, Properties
    If no identifying "name key" is found, the table will be a single column table with the properties.

    NOTE: nesting is done as needed
    """
    caption = FOUND_ITEMS.format(len(items)) if outer else None
    name_key = _get_name_key(items[0])
    if not name_key:
        # without identifiers just create table with one "Values" column
        table = RichTable(VALUES, outer=outer, show_lines=True, caption=caption)
        for item in items:
            table.add_row(_table_cell_value(item))
        return table

    # create a table with identifier in left column, and rest of data in right column
    name_label = name_key[0].upper() + name_key[1:]
    fields = [name_label, PROPERTIES]
    table = RichTable(*fields, outer=outer, show_lines=True, caption=caption)
    for item in items:
        # id may be an int, so convert to string before truncating
        name = str(item.pop(name_key, UNKNOWN))
        body = _table_cell_value(item)
        table.add_row(_truncate(name, KEY_MAX_LEN), body)

    return table


def _create_object_table(obj: dict[Any, Any], outer: bool) -> RichTable:
    """Creates a table of a dictionary object.

    NOTE: nesting is done in the right column as needed.
    """
    table = RichTable(*OBJECT_HEADERS, outer=outer, show_lines=False)
    for k, v in obj.items():
        name = str(k)
        table.add_row(_truncate(name, KEY_MAX_LEN), _table_cell_value(v))

    return table


def _table_cell_value(obj: Any) -> Any:
    """Creates the "inner" value for a table cell.

    Depending on the input value type, the cell may look different. If a dict, or list[dict],
    an inner table is created. Otherwise, the object is converted to a printable value.
    """
    value: Any = None
    if isinstance(obj, dict):
        value = _create_object_table(obj, outer=False)
    elif isinstance(obj, list) and obj:
        if isinstance(obj[0], dict):
            value = _create_list_table(obj, outer=False)
        else:
            values = [str(x) for x in obj]
            s = str(", ".join(values))
            value = _truncate(s, VALUE_MAX_LEN)
    else:
        s = str(obj)
        max_len = URL_MAX_LEN if _is_url(s) else VALUE_MAX_LEN
        value = _truncate(s, max_len)

    return value


def rich_table_factory(obj: Any) -> RichTable:
    """Create a RichTable (alias for rich.table.Table) from the object."""
    if isinstance(obj, dict):
        return _create_object_table(obj, outer=True)

    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        return _create_list_table(obj, outer=True)

    raise ValueError(f"Unable to create table for type {type(obj).__name__}")
