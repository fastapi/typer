import typer


def main(name: str, age: int = 20, height_meters: float = 1.89, female: bool = True):
    typer.echo(f"NAME is {name}, of type: {type(name)}")
    typer.echo(f"--age is {age}, of type: {type(age)}")
    typer.echo(f"--height-meters is {height_meters}, of type: {type(height_meters)}")
    typer.echo(f"--female is {female}, of type: {type(female)}")


if __name__ == "__main__":
    typer.run(main)
