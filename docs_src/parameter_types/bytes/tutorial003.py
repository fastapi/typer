import typer


def main(token: bytes = typer.Option(..., encoding="ascii", errors="replace")):
    # Option configured with ascii encoding and errors=replace
    print(f"Token: {token!r}")


if __name__ == "__main__":
    typer.run(main)
