from pathlib import Path

app = "not a Typer app"


def some_function(name: str = "World"):
    print(f"Hello {name} from {Path('.').name or 'here'}")
