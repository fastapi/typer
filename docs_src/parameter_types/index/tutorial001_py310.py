import typer

app = typer.Typer()


@app.command()
def main(name: str, age: int = 20, height_meters: float = 1.89, female: bool = True):
    print(f"NAME is {name}, of type: {type(name)}")
    print(f"--age is {age}, of type: {type(age)}")
    print(f"--height-meters is {height_meters}, of type: {type(height_meters)}")
    print(f"--female is {female}, of type: {type(female)}")


if __name__ == "__main__":
    app()
