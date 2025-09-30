import typer


def main(data: bytes):
    # Default encoding is UTF-8
    print(f"Bytes: {data!r}")


if __name__ == "__main__":
    typer.run(main)
