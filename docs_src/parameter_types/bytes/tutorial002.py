import typer


def main(data: bytes = typer.Argument(..., encoding="latin-1")):
    # Argument configured to use latin-1
    print(f"Bytes (latin-1): {data!r}")


if __name__ == "__main__":
    typer.run(main)
