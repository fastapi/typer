from gettext import gettext
from typing import Any, Dict, List, Optional

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


class TableConfig:
    """This data class provides a means for customizing the table outputs.

    The defaults provide a standard look and feel, but can be overridden to all customization.
    """

    def __init__(
        self,
        items_label: str = ITEMS,
        property_label: str = PROPERTY,
        properties_label: str = PROPERTIES,
        value_label: str = VALUE,
        values_label: str = VALUES,
        unknown_label: str = UNKNOWN,
        items_caption: str = FOUND_ITEMS,
        url_prefixes: List[str] = URL_PREFIXES,
        url_max_len: int = URL_MAX_LEN,
        key_fields: List[str] = KEY_FIELDS,
        key_max_len: int = KEY_MAX_LEN,
        value_max_len: int = VALUE_MAX_LEN,
        row_properties: Dict[str, Any] = DEFAULT_ROW_PROPS,
    ):
        self.items_label = items_label
        self.property_label = property_label
        self.properties_label = properties_label
        self.value_label = value_label
        self.values_label = values_label
        self.unknown_label = unknown_label
        self.items_caption = items_caption
        self.url_prefixes = url_prefixes
        self.url_max_len = url_max_len
        self.key_fields = key_fields
        self.key_max_len = key_max_len
        self.value_max_len = value_max_len
        self.row_properties = row_properties


class RichTable(Table):
    """
    This is wrapper around the rich.Table to provide some methods for adding complex items.
    """

    def __init__(
        self,
        *args: Any,
        outer: bool = True,
        row_props: Dict[str, Any] = DEFAULT_ROW_PROPS,
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


def _get_name_key(item: Dict[Any, Any], key_fields: List[str]) -> Optional[str]:
    """Attempts to find an identifying value."""
    for k in key_fields:
        key = str(k)
        if key in item:
            return key

    return None


def _is_url(s: str, url_prefixes: List[str]) -> bool:
    """Rudimentary check for somethingt starting with URL prefix"""
    return any(s.startswith(p) for p in url_prefixes)


def _create_list_table(
    items: List[Dict[Any, Any]], outer: bool, config: TableConfig
) -> RichTable:
    """Creates a table from a list of dictionary items.

    If an identifying "name key" is found (in the first entry), the table will have 2 columns: name, Properties
    If no identifying "name key" is found, the table will be a single column table with the properties.

    NOTE: nesting is done as needed
    """
    caption = config.items_caption.format(len(items)) if outer else None
    name_key = _get_name_key(items[0], config.key_fields)
    if not name_key:
        # without identifiers just create table with one "Values" column
        table = RichTable(
            config.values_label,
            outer=outer,
            show_lines=True,
            caption=caption,
            row_props=config.row_properties,
        )
        for item in items:
            table.add_row(_table_cell_value(item, config))
        return table

    # create a table with identifier in left column, and rest of data in right column
    name_label = name_key[0].upper() + name_key[1:]
    fields = [name_label, config.properties_label]
    table = RichTable(
        *fields,
        outer=outer,
        show_lines=True,
        caption=caption,
        row_props=config.row_properties,
    )
    for item in items:
        # id may be an int, so convert to string before truncating
        name = str(item.pop(name_key, config.unknown_label))
        body = _table_cell_value(item, config)
        table.add_row(_truncate(name, config.key_max_len), body)

    return table


def _create_object_table(
    obj: Dict[Any, Any], outer: bool, config: TableConfig
) -> RichTable:
    """Creates a table of a dictionary object.

    NOTE: nesting is done in the right column as needed.
    """
    headers = [config.property_label, config.value_label]
    table = RichTable(
        *headers, outer=outer, show_lines=False, row_props=config.row_properties
    )
    for k, v in obj.items():
        name = str(k)
        table.add_row(_truncate(name, config.key_max_len), _table_cell_value(v, config))

    return table


def _table_cell_value(obj: Any, config: TableConfig) -> Any:
    """Creates the "inner" value for a table cell.

    Depending on the input value type, the cell may look different. If a dict, or list[dict],
    an inner table is created. Otherwise, the object is converted to a printable value.
    """
    value: Any = None
    if isinstance(obj, dict):
        value = _create_object_table(obj, outer=False, config=config)
    elif isinstance(obj, list) and obj:
        if isinstance(obj[0], dict):
            value = _create_list_table(obj, outer=False, config=config)
        else:
            values = [str(x) for x in obj]
            s = str(", ".join(values))
            value = _truncate(s, config.value_max_len)
    else:
        s = str(obj)
        max_len = (
            config.url_max_len
            if _is_url(s, config.url_prefixes)
            else config.value_max_len
        )
        value = _truncate(s, max_len)

    return value


def rich_table_factory(obj: Any, config: TableConfig = TableConfig()) -> RichTable:
    """Create a RichTable (alias for rich.table.Table) from the object."""
    if isinstance(obj, dict):
        return _create_object_table(obj, outer=True, config=config)

    if isinstance(obj, list) and obj and isinstance(obj[0], dict):
        return _create_list_table(obj, outer=True, config=config)

    # this is a list of "simple" properties
    if (
        isinstance(obj, list)
        and obj
        and all(
            item is None or isinstance(item, (str, float, bool, int)) for item in obj
        )
    ):
        caption = config.items_caption.format(len(obj))
        table = RichTable(
            config.items_label,
            outer=True,
            show_lines=True,
            caption=caption,
            row_props=config.row_properties,
        )
        for item in obj:
            table.add_row(_table_cell_value(item, config))
        return table

    raise ValueError(f"Unable to create table for type {type(obj).__name__}")
