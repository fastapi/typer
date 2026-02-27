import gitlab
import typer

app = typer.Typer(pretty_exceptions_suppress=[gitlab])


@app.command()
def main():
    gitlab_client = gitlab.Gitlab()

    # This will raise an exception if not authenticated:
    #     GitlabAuthenticationError: 401: 401 Unauthorized
    # But the traceback will not show any lines from the gitlab module!
    print(gitlab_client.pagesdomains.list())


if __name__ == "__main__":
    app()
