import typer

import pydantic


class User(pydantic.BaseModel):
    id: int
    name: str = "Jane Doe"


def main(num: int, user: User):
    print(num, type(num))
    print(user, type(user))


if __name__ == "__main__":
    typer.run(main)
