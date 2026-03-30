from typing import Annotated

import typer
from typer.testing import CliRunner

runner = CliRunner()


def test_argument_parsing_basic():
    """测试基本命令行参数解析"""
    app = typer.Typer()

    @app.command()
    def greet(name: str, age: int):
        print(f"Hello {name}, you are {age} years old")

    result = runner.invoke(app, ["Alice", "30"])
    assert result.exit_code == 0
    assert "Hello Alice, you are 30 years old" in result.output


def test_argument_with_default_value():
    """测试带默认值的命令行参数"""
    app = typer.Typer()

    @app.command()
    def greet(name: str = "World", age: int = 42):
        print(f"Hello {name}, you are {age} years old")

    # 测试默认值 - 不带参数调用（有默认值的参数会变成选项）
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World, you are 42 years old" in result.output

    # 测试通过选项方式提供参数
    result = runner.invoke(app, ["--name", "Bob", "--age", "30"])
    assert result.exit_code == 0
    assert "Hello Bob, you are 30 years old" in result.output

    # 使用短选项
    result = runner.invoke(app, ["--name", "Charlie"])
    assert result.exit_code == 0
    assert "Hello Charlie, you are 42 years old" in result.output


def test_annotated_argument_with_default():
    """测试 Annotated 类型的参数带默认值"""
    app = typer.Typer()

    @app.command()
    def cmd(
        name: Annotated[str, typer.Argument(help="The name to greet")] = "Guest",
        count: Annotated[int, typer.Argument(help="Repeat count")] = 1,
    ):
        for _ in range(count):
            print(f"Hello {name}")

    # 测试默认值
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert result.output == "Hello Guest\n"

    # 测试传递参数
    result = runner.invoke(app, ["Alice", "3"])
    assert result.exit_code == 0
    assert result.output == "Hello Alice\nHello Alice\nHello Alice\n"


def test_option_parsing_basic():
    """测试选项参数解析"""
    app = typer.Typer()

    @app.command()
    def greet(name: str = typer.Option("World", help="The name to greet")):
        print(f"Hello {name}")

    # 默认值
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello World" in result.output

    # 长选项
    result = runner.invoke(app, ["--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello Alice" in result.output


def test_option_with_short_name():
    """测试带短名称的选项"""
    app = typer.Typer()

    @app.command()
    def greet(
        name: str = typer.Option("World", "--name", "-n", help="The name to greet"),
        verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode"),
    ):
        if verbose:
            print(f"[VERBOSE] Hello {name}!")
        else:
            print(f"Hello {name}")

    # 短选项
    result = runner.invoke(app, ["-n", "Bob"])
    assert result.exit_code == 0
    assert "Hello Bob" in result.output

    # 标志选项
    result = runner.invoke(app, ["-v", "-n", "Charlie"])
    assert result.exit_code == 0
    assert "[VERBOSE] Hello Charlie!" in result.output


def test_mixed_args_and_options():
    """测试位置参数和选项参数混合使用"""
    app = typer.Typer()

    @app.command()
    def compute(
        operation: str,
        numbers: list[int] = typer.Argument(..., help="Numbers to process"),
        round_result: bool = typer.Option(False, "--round", "-r"),
    ):
        if operation == "sum":
            result = sum(numbers)
        elif operation == "max":
            result = max(numbers)
        else:
            result = 0
        if round_result:
            result = int(round(result))
        print(f"Result: {result}")

    # 基本操作
    result = runner.invoke(app, ["sum", "1", "2", "3"])
    assert result.exit_code == 0
    assert "Result: 6" in result.output

    # 带选项
    result = runner.invoke(app, ["max", "1", "5", "3", "--round"])
    assert result.exit_code == 0
    assert "Result: 5" in result.output


def test_help_output_format():
    """测试帮助信息输出格式"""
    app = typer.Typer()

    @app.command("greet")
    def greet_cmd(
        name: str = typer.Argument("World", help="The name to greet"),
        loud: bool = typer.Option(False, help="Greet loudly"),
    ):
        """Greet someone by name."""
        greeting = f"Hello {name}"
        if loud:
            greeting = greeting.upper() + "!!!"
        print(greeting)

    result = runner.invoke(app, ["greet", "--help"])
    assert result.exit_code == 0
    # 检查帮助信息的关键部分
    assert "Greet someone by name." in result.output
    assert "Arguments" in result.output
    assert "Options" in result.output
    assert "--loud" in result.output
    assert "Greet loudly" in result.output


def test_help_output_with_required_args():
    """测试必填参数的帮助输出"""
    app = typer.Typer()

    @app.command()
    def hello(
        name: str = typer.Argument(..., help="The name of the user to greet"),
        formal: bool = typer.Option(False, help="Use formal greeting"),
    ):
        """Say hello to someone."""
        if formal:
            print(f"Good day, {name}.")
        else:
            print(f"Hello {name}!")

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "[required]" in result.output
    assert "Say hello to someone." in result.output
    assert "The name of the user to greet" in result.output


def test_invalid_numeric_input():
    """测试非法数字输入"""
    app = typer.Typer()

    @app.command()
    def calculate(age: int, price: float):
        print(f"Age: {age}, Price: {price}")

    # 传入非数字给整型参数
    result = runner.invoke(app, ["not-a-number", "10.5"])
    assert result.exit_code != 0
    assert "age" in result.output.lower() or "integer" in result.output.lower()

    # 传入非数字给浮点参数
    result = runner.invoke(app, ["25", "not-a-float"])
    assert result.exit_code != 0
    assert "float" in result.output.lower() or "price" in result.output.lower()


def test_argument_count_mismatch():
    """测试参数数量不匹配"""
    app = typer.Typer()

    @app.command()
    def three_args(a: str, b: str, c: str):
        print(f"{a} {b} {c}")

    # 参数不足
    result = runner.invoke(app, ["only", "two"])
    assert result.exit_code != 0
    assert "argument" in result.output.lower() or "missing" in result.output.lower()

    # 参数过多
    result = runner.invoke(app, ["one", "two", "three", "four"])
    assert result.exit_code != 0
    assert "unexpected" in result.output.lower() or "extra" in result.output.lower()


def test_invalid_choice_enum():
    """测试枚举类型的非法输入"""
    from enum import Enum

    class Color(str, Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    app = typer.Typer()

    @app.command()
    def paint(color: Color = Color.RED):
        print(f"Painting with {color.value}")

    # 测试有效输入
    result = runner.invoke(app, ["--color", "green"])
    assert result.exit_code == 0
    assert "Painting with green" in result.output

    # 测试无效输入
    result = runner.invoke(app, ["--color", "yellow"])
    assert result.exit_code != 0
    assert "red" in result.output.lower()
    assert "green" in result.output.lower()
    assert "blue" in result.output.lower()


def test_boundary_values_numeric():
    """测试边界值输入"""
    app = typer.Typer()

    @app.command()
    def set_level(level: int = typer.Argument(..., min=0, max=100)):
        print(f"Level set to {level}")

    # 有效边界值
    result = runner.invoke(app, ["0"])
    assert result.exit_code == 0
    assert "Level set to 0" in result.output

    result = runner.invoke(app, ["100"])
    assert result.exit_code == 0
    assert "Level set to 100" in result.output

    # 使用 -- 标记选项结束，后面的 -1 会被当作参数
    result = runner.invoke(app, ["--", "-1"])
    assert result.exit_code != 0
    assert (
        "0" in result.output
        or "minimum" in result.output.lower()
        or "less" in result.output.lower()
    )

    # 测试超出最大值
    result = runner.invoke(app, ["101"])
    assert result.exit_code != 0
    assert (
        "100" in result.output
        or "maximum" in result.output.lower()
        or "greater" in result.output.lower()
    )


def test_required_option_missing():
    """测试缺失必填选项的报错提示"""
    app = typer.Typer()

    @app.command()
    def login(
        username: str = typer.Option(..., help="Username for login"),
        password: str = typer.Option(..., help="Password for login"),
    ):
        print(f"Logging in as {username}")

    # 不提供必填选项
    result = runner.invoke(app)
    assert result.exit_code != 0
    # 检查报错是否包含"required"或"missing"等关键词
    assert (
        "required" in result.output.lower()
        or "missing" in result.output.lower()
        or "username" in result.output.lower()
    )


def test_type_conversion_error_message():
    """测试类型转换错误提示"""
    app = typer.Typer()

    @app.command()
    def process_item(
        item_id: int,
        score: float,
        active: bool,
    ):
        print(f"Item {item_id}: score={score}, active={active}")

    # 测试整数转换错误
    result = runner.invoke(app, ["not-an-int", "3.14", "True"])
    assert result.exit_code != 0
    assert (
        "item_id" in result.output.lower()
        or "int" in result.output.lower()
        or "integer" in result.output.lower()
    )

    # 测试浮点数转换错误
    result = runner.invoke(app, ["123", "not-a-float", "False"])
    assert result.exit_code != 0
    assert (
        "score" in result.output.lower()
        or "float" in result.output.lower()
        or "not-a-float" in result.output.lower()
    )


def test_help_descriptions():
    """测试帮助信息中的描述文本"""
    app = typer.Typer(help="A test CLI application")

    @app.command("create", help="Create a new item")
    def create_item(
        name: str = typer.Argument(..., help="Name of the item"),
        description: str = typer.Option("", help="Description of the item"),
        priority: int = typer.Option(1, help="Priority level (1-5)"),
    ):
        print(f"Created {name}: {description} (priority: {priority})")

    @app.command("delete", help="Delete an item")
    def delete_item(
        item_id: int = typer.Argument(..., help="ID of the item to delete"),
    ):
        print(f"Deleted item {item_id}")

    # 测试主程序帮助（当有多个子命令时）
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "A test CLI application" in result.output or "create" in result.output

    # 测试子命令帮助
    result = runner.invoke(app, ["create", "--help"])
    assert result.exit_code == 0
    assert "Create a new item" in result.output
    assert "Name of the item" in result.output
    assert "Description of the item" in result.output
    assert "Priority level" in result.output


def test_unknown_option_error():
    """测试未知选项的错误提示"""
    app = typer.Typer()

    @app.command()
    def simple(name: str = "World"):
        print(f"Hello {name}")

    result = runner.invoke(app, ["--unknown-option"])
    assert result.exit_code != 0
    assert (
        "--unknown-option" in result.output
        or "unrecognized" in result.output.lower()
        or "unknown" in result.output.lower()
    )


def test_empty_string_vs_none():
    """测试空字符串与None值的区别"""
    app = typer.Typer()

    @app.command()
    def test_opt(
        value: str | None = typer.Option(None, help="Optional string value"),
    ):
        if value is None:
            print("Value is None")
        elif value == "":
            print("Value is empty string")
        else:
            print(f"Value is: {value}")

    # 不提供选项
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Value is None" in result.output

    # 提供空字符串
    result = runner.invoke(app, ["--value", ""])
    assert result.exit_code == 0
    assert "Value is empty string" in result.output

    # 提供实际值
    result = runner.invoke(app, ["--value", "hello"])
    assert result.exit_code == 0
    assert "Value is: hello" in result.output
