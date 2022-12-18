import json
from typing import Any, Dict, Optional, Union

import click
import typer


class JsonParamType(click.ParamType):
    name: str = "json"

    def convert(
        self,
        value: Optional[Union[Dict[Any, Any], str, bytes]],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Optional[Dict[Any, Any]]:
        if isinstance(value, dict) or value is None:
            return value  # pragma: nocover
        try:
            if isinstance(value, (str, bytes)):
                return json.loads(value)
            else:
                self.fail(
                    f"{value!r} was not a str, bytes or None.", param, ctx
                )  # pragma: nocover
        except OSError as e:
            self.fail([*e.args, None][0], param, ctx)  # pragma: nocover
        except json.JSONDecodeError as e:
            self.fail(f"Bad JSON: {[*e.args, None][0]}", param, ctx)


JSON = JsonParamType()


def main(data: dict = typer.Option(..., param_type=JSON)):
    if "what_i_like" in data:
        typer.echo(f"You like {data['what_i_like']}? Me too!")


if __name__ == "__main__":
    typer.run(main)
