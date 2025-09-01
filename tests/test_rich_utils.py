import json
from copy import deepcopy

import pytest
import typer
import typer.completion
import yaml
from typer.rich_utils import OutputFormat, TableConfig, print_rich_object
from typer.testing import CliRunner

runner = CliRunner()


def test_rich_utils_click_rewrapp():
    app = typer.Typer(rich_markup_mode="markdown")

    @app.command()
    def main():
        """
        \b
        Some text

        Some unwrapped text
        """
        print("Hello World")

    @app.command()
    def secondary():
        """
        \b
        Secondary text

        Some unwrapped text
        """
        print("Hello Secondary World")

    result = runner.invoke(app, ["--help"])
    assert "Some text" in result.stdout
    assert "Secondary text" in result.stdout
    assert "\b" not in result.stdout
    result = runner.invoke(app, ["main"])
    assert "Hello World" in result.stdout
    result = runner.invoke(app, ["secondary"])
    assert "Hello Secondary World" in result.stdout


def test_rich_help_no_commands():
    """Ensure that the help still works for a Typer instance with no commands, but with a callback."""
    app = typer.Typer(help="My cool Typer app")

    @app.callback(invoke_without_command=True, no_args_is_help=True)
    def main() -> None:
        return None  # pragma: no cover

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Show this message" in result.stdout


def test_rich_doesnt_print_None_default():
    app = typer.Typer(rich_markup_mode="rich")

    @app.command()
    def main(
        name: str,
        option_1: str = typer.Option(
            "option_1_default",
        ),
        option_2: str = typer.Option(
            ...,
        ),
    ):
        print(f"Hello {name}")
        print(f"First: {option_1}")
        print(f"Second: {option_2}")

    result = runner.invoke(app, ["--help"])
    assert "Usage" in result.stdout
    assert "name" in result.stdout
    assert "option-1" in result.stdout
    assert "option-2" in result.stdout
    assert result.stdout.count("[default: None]") == 0
    result = runner.invoke(app, ["Rick", "--option-2=Morty"])
    assert "Hello Rick" in result.stdout
    assert "First: option_1_default" in result.stdout
    assert "Second: Morty" in result.stdout


DATA = [
    {"name": "sna", "prop1": 1, "prop B": None, "blah": "zay"},
    {
        "name": "foo",
        "prop2": 2,
        "prop B": True,
    },
    {
        "name": "bar",
        1: "inverse",
    },
]


EXPECTED_JSON = json.dumps(DATA, indent=2)
EXPECTED_YAML = yaml.dump(DATA)
EXPECTED_TEXT = """\
┏━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Name ┃ Properties     ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━┩
│ sna  │  prop1   1     │
│      │  prop B  None  │
│      │  blah    zay   │
├──────┼────────────────┤
│ foo  │  prop2   2     │
│      │  prop B  True  │
├──────┼────────────────┤
│ bar  │  1  inverse    │
└──────┴────────────────┘
Found 3 items"""

CONFIGED_TEXT = """\
┏━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Name ┃          Inner ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━┩
│  sna │   prop1     1  │
│      │  prop B  None  │
│      │    blah   zay  │
├──────┼────────────────┤
│  foo │   prop2     2  │
│      │  prop B  True  │
├──────┼────────────────┤
│  bar │  1  inverse    │
└──────┴────────────────┘
This shows 3 items"""


def prepare(s: str) -> str:
    """
    Return string with '.' in place of all non-ASCII characters (other than newlines).

    This avoids differences in terminal output for non-ASCII characters like, table borders. The
    newline is passed through to let original look "almost" like the modified version.
    """
    return "".join(
        char if 31 < ord(char) < 127 or char == "\n" else "." for char in s
    ).rstrip()


@pytest.mark.parametrize(
    "output_format, expected",
    [
        pytest.param("json", EXPECTED_JSON, id="json"),
        pytest.param("yaml", EXPECTED_YAML, id="yaml"),
        pytest.param("text", EXPECTED_TEXT, id="text"),
    ],
)
def test_rich_object_data(output_format, expected):
    app = typer.Typer()

    @app.command()
    def print_rich_data(output_format: OutputFormat):
        print_rich_object(deepcopy(DATA), out_fmt=output_format)

    result = runner.invoke(app, [output_format])
    assert result.exit_code == 0
    output = prepare(result.stdout)
    prepared = prepare(expected)
    assert output == prepared


@pytest.mark.parametrize(
    "output_format, expected",
    [
        pytest.param("json", "null\n", id="json"),
        pytest.param("yaml", "null\n...\n\n", id="yaml"),
        pytest.param("text", "Nothing found\n", id="text"),
    ],
)
def test_rich_object_none(output_format, expected):
    app = typer.Typer()

    @app.command()
    def print_rich_none(output_format: OutputFormat):
        print_rich_object(None, out_fmt=output_format)

    result = runner.invoke(app, [output_format])
    assert result.exit_code == 0
    output = prepare(result.stdout)
    prepared = prepare(expected)
    assert output == prepared


def test_rich_object_config():
    app = typer.Typer()

    @app.command()
    def print_rich_data():
        config = TableConfig(
            row_properties={"justify": "right", "no_wrap": True, "overflow": "ignore"},
            properties_label="Inner",
            items_caption="This shows {} items",
        )
        print_rich_object(DATA, config=config)

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    output = prepare(result.stdout)
    prepared = prepare(deepcopy(CONFIGED_TEXT))
    assert output == prepared
