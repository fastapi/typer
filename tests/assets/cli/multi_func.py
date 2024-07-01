message = "Stuff"


def say_stuff():
    print(message)


def main(name: str = "World"):
    """
    Say hi to someone, by default to the World.
    """
    print(f"Hello {name}")
