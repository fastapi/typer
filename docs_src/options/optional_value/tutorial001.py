import typer


def main(name: str, lastname: str, greeting: bool | str = "formal"):
    if not greeting:
        return

    if greeting == "formal":
        print(f"Hello {name} {lastname}")

    elif greeting == "casual":
        print(f"Hi {name} !")

    else:
        raise ValueError(f"Invalid greeting '{greeting}'")


if __name__ == "__main__":
    typer.run(main)
