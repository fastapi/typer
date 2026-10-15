from imported_by_other import hello
from subdir.imported_nested import echo


def main(name: str):
    hello(name)
    echo(name)
