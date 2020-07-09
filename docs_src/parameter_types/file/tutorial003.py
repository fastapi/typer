import typer


def main(file: typer.FileBinaryRead = typer.Option(...)):
    processed_total = 0
    for bytes_chunk in file:
        # Process the bytes in bytes_chunk
        processed_total += len(bytes_chunk)
        typer.echo(f"Processed bytes total: {processed_total}")


if __name__ == "__main__":
    typer.run(main)
