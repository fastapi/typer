import json

import typer
from typing_extensions import Annotated


def main(user_info: Annotated[dict, typer.Option()]):
    print(f"User Info: {json.dumps(user_info)}")


if __name__ == "__main__":
    typer.run(main)
