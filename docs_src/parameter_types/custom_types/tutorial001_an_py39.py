from typing import Annotated

import typer


class CustomClass:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"<CustomClass: value={self.value}>"


def parse_custom_class(value: str):
    return CustomClass(value * 2)


app = typer.Typer()


@app.command()
def main(
    custom_arg: Annotated[CustomClass, typer.Argument(parser=parse_custom_class)],
    custom_opt: Annotated[CustomClass, typer.Option(parser=parse_custom_class)] = "Foo",
):
    print(f"custom_arg is {custom_arg}")
    print(f"--custom-opt is {custom_opt}")


if __name__ == "__main__":
    app()
