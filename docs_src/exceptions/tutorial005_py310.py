import urllib.request

import typer

app = typer.Typer(pretty_exceptions_suppress=[urllib.request])


@app.command()
def main():
    urllib.request.urlopen("unknown://example.com")


if __name__ == "__main__":
    app()
