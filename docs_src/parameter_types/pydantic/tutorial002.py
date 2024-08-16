from typing import Optional

import typer

import pydantic


class Pet(pydantic.BaseModel):
    name: str
    species: str


class Person(pydantic.BaseModel):
    name: str
    age: Optional[float] = None
    pet: Pet


def main(person: Person):
    print(person, type(person))


if __name__ == "__main__":
    typer.run(main)
