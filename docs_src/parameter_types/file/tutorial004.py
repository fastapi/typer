import typer


def main(file: typer.FileBinaryWrite = typer.Option(...)):
    first_line_str = "some settings\n"
    # You cannot write str directly to a binary file, you have to encode it to get bytes
    first_line_bytes = first_line_str.encode("utf-8")
    # Then you can write the bytes
    file.write(first_line_bytes)
    # This is already bytes, it starts with b"
    second_line = b"la cig\xc3\xbce\xc3\xb1a trae al ni\xc3\xb1o"
    file.write(second_line)
    typer.echo("Binary file written")


if __name__ == "__main__":
    typer.run(main)
