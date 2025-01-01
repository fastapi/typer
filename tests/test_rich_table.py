from copy import deepcopy
from itertools import zip_longest

import pytest
from rich.box import HEAVY_HEAD
from typer.rich_table import RichTable, TableConfig, rich_table_factory

SIMPLE_DICT = {
    "abc": "def",
    "ghi": False,
    "jkl": ["mno", "pqr", "stu"],
    "vwx": [1, 2, 4],
    2: 3,
    "yxa": None,
}

LONG_VALUES = {
    "mid-url": "https://typer.tiangolo.com/virtual-environments/#install-packages-directly",
    "really looooooooooooooooooonnnng key value": "sna",
    "long value": "a" * 75,
    "long": "ftp://typer.tiangolo.com/virtual-environments/#install-packages-directly?12345678901234568901234567890123",
}

INNER_LIST = {
    "prop 1": "simple",
    "prOp B": [
        {"name": "sna", "abc": "def", "ghi": True},
        {"name": "foo", "abc": "def", "ghi": None},
        {"name": "bar", "abc": "def", "ghi": 1.2345},
        {"abc": "def", "ghi": "blah"},
    ],
    "Prop III": None,
}


def test_rich_table_defaults_outer():
    columns = ["col 1", "Column B", "III"]
    uut = RichTable(*columns, outer=True)
    assert len(uut.columns) == len(columns)
    assert uut.highlight
    assert uut.row_styles == []
    assert uut.caption_justify == "left"
    assert uut.border_style is None
    assert uut.leading == 0

    assert uut.show_header
    assert uut.show_edge
    assert uut.box == HEAVY_HEAD

    for name, column in zip_longest(columns, uut.columns):
        assert column.header == name
        assert column.overflow == "ignore"
        assert column.no_wrap
        assert column.justify == "left"


def test_rich_table_defaults_inner():
    columns = ["col 1", "Column B", "III"]
    uut = RichTable(*columns, outer=False)
    assert len(uut.columns) == len(columns)
    assert uut.highlight
    assert uut.row_styles == []
    assert uut.caption_justify == "left"
    assert uut.border_style is None
    assert uut.leading == 0

    assert not uut.show_header
    assert not uut.show_edge
    assert uut.box is None

    for name, column in zip_longest(columns, uut.columns):
        assert column.header == name
        assert column.overflow == "ignore"
        assert column.no_wrap
        assert column.justify == "left"


def test_create_table_not_obj():
    with pytest.raises(ValueError) as excinfo:
        rich_table_factory([1, 2, 3])

    assert excinfo.match("Unable to create table for type list")


def test_create_table_simple_dict():
    uut = rich_table_factory(SIMPLE_DICT)

    # basic outer table stuff for object
    assert len(uut.columns) == 2
    assert uut.show_header
    assert uut.show_edge
    assert not uut.show_lines

    # data-driven info
    assert uut.row_count == 6


def test_create_table_list_nameless_dict():
    items = [SIMPLE_DICT, SIMPLE_DICT, {"foo": "bar"}]
    uut = rich_table_factory(items)

    # basic outer table stuff for object
    assert len(uut.columns) == 1
    assert uut.show_header
    assert uut.show_edge
    assert uut.show_lines

    # data-driven info
    assert uut.row_count == len(items)


def test_create_table_list_named_dict():
    names = ["sna", "foo", "bar", "baz"]
    items = []
    for name in names:
        item = deepcopy(SIMPLE_DICT)
        item["name"] = name
        items.append(item)

    uut = rich_table_factory(items)

    # basic outer table stuff for object
    assert len(uut.columns) == 2
    assert uut.show_header
    assert uut.show_edge
    assert uut.show_lines

    # data-driven info
    assert uut.row_count == len(items)
    assert uut.caption == f"Found {len(items)} items"

    col0 = uut.columns[0]
    col1 = uut.columns[1]
    for left, right, name, item in zip_longest(col0._cells, col1._cells, names, items):
        assert left == name
        inner_keys = right.columns[0]._cells
        item_keys = [str(k) for k in item.keys() if k != "name"]
        assert inner_keys == item_keys


def test_create_table_truncted():
    data = deepcopy(LONG_VALUES)

    uut = rich_table_factory(data)

    assert uut.row_count == 4
    col0 = uut.columns[0]
    col1 = uut.columns[1]

    assert col0.header == "Property"
    assert col1.header == "Value"

    # url has longer length than "normal" fields
    index = 0
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "mid-url"
    assert (
        right
        == "https://typer.tiangolo.com/virtual-environments/#install-packages-directly"
    )

    # keys get truncated at 35 characters
    index = 1
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "really looooooooooooooooooonnnng..."
    assert right == "sna"

    # non-url values get truncated at 50 characters
    index = 2
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "long value"
    assert right == "a" * 47 + "..."

    # really long urls get truncated at 100 characters
    index = 3
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "long"
    assert (
        right
        == "ftp://typer.tiangolo.com/virtual-environments/#install-packages-directly?123456789012345689012345..."
    )


def test_create_table_inner_list():
    data = deepcopy(INNER_LIST)

    uut = rich_table_factory(data)
    assert uut.row_count == 3
    assert len(uut.columns) == 2
    col0 = uut.columns[0]
    col1 = uut.columns[1]

    left = col0._cells[0]
    right = col1._cells[0]
    assert left == "prop 1"
    assert right == "simple"

    left = col0._cells[2]
    right = col1._cells[2]
    assert left == "Prop III"
    assert right == "None"

    left = col0._cells[1]
    inner = col1._cells[1]
    assert left == "prOp B"
    assert len(inner.columns) == 2
    assert inner.row_count == 4
    names = inner.columns[0]._cells
    assert names == ["sna", "foo", "bar", "Unknown"]


def test_create_table_config_truncated():
    config = TableConfig(url_max_len=16, value_max_len=20, key_max_len=4)
    data = deepcopy(LONG_VALUES)

    uut = rich_table_factory(data, config)

    assert uut.row_count == 4
    col0 = uut.columns[0]
    col1 = uut.columns[1]

    # keys truncated at 4 characters, and urls at 14
    index = 0
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "m..."
    assert right == "https://typer..."

    # keys truncated at 4 characters, and short fields are not truncated
    index = 1
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "r..."
    assert right == "sna"

    # non-url values get truncated at 20 characters
    index = 2
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "l..."
    assert right == "a" * 17 + "..."

    # really long urls get truncated at 16 characters
    index = 3
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "l..."
    assert right == "ftp://typer.t..."


def test_create_table_config_fields():
    config = TableConfig(
        url_max_len=16,
        value_max_len=50,
        key_max_len=100,
        url_prefixes=["https://"],  # do NOT recognize ftp as a prefix
        property_label="foo",
        value_label="bar",
    )
    data = deepcopy(LONG_VALUES)

    uut = rich_table_factory(data, config)

    assert uut.row_count == 4
    col0 = uut.columns[0]
    col1 = uut.columns[1]

    assert col0.header == "foo"
    assert col1.header == "bar"

    # keys truncated at 4 characters, and urls at 16
    index = 0
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "mid-url"
    assert right == "https://typer..."

    # keys truncated at 4 characters, and short fields are not truncated
    index = 1
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "really looooooooooooooooooonnnng key value"
    assert right == "sna"

    # non-url values get truncated at 20 characters
    index = 2
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "long value"
    assert right == "a" * 47 + "..."

    # ftp is NOT a URL, so it gets truncated at 50 characerts
    index = 3
    left = col0._cells[index]
    right = col1._cells[index]
    assert left == "long"
    assert right == "ftp://typer.tiangolo.com/virtual-environments/#..."


def test_create_table_config_inner_list():
    data = deepcopy(INNER_LIST)
    config = TableConfig(
        key_fields=["ghi"],
        properties_label="Different",
    )

    uut = rich_table_factory(data, config)
    assert uut.row_count == 3
    assert len(uut.columns) == 2
    col0 = uut.columns[0]
    col1 = uut.columns[1]

    left = col0._cells[0]
    right = col1._cells[0]
    assert left == "prop 1"
    assert right == "simple"

    left = col0._cells[2]
    right = col1._cells[2]
    assert left == "Prop III"
    assert right == "None"

    left = col0._cells[1]
    inner = col1._cells[1]
    assert left == "prOp B"
    assert len(inner.columns) == 2
    assert inner.columns[0].header == "Ghi"
    assert inner.columns[1].header == "Different"
    assert inner.row_count == 4
    names = inner.columns[0]._cells
    assert names == ["True", "None", "1.2345", "blah"]
