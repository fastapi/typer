import logging
import os
import re
import shutil
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import typer

logging.basicConfig(level=logging.INFO)

mkdocs_name = "mkdocs.yml"
docs_path = Path("docs")
en_docs_path = Path("")

app = typer.Typer()


@app.callback()
def callback() -> None:
    # For MacOS with Cairo
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/lib"


def generate_readme_content() -> str:
    en_index = en_docs_path / "docs" / "index.md"
    content = en_index.read_text("utf-8")
    match_pre = re.search(r"</style>\n\n", content)
    if not match_pre:
        raise RuntimeError("Couldn't find pre section (<style>) in index.md")
    frontmatter_end = match_pre.end()
    new_content = content[frontmatter_end:]
    # Remove content between <!-- only-mkdocs --> and <!-- /only-mkdocs -->
    new_content = re.sub(
        r"<!-- only-mkdocs -->.*?<!-- /only-mkdocs -->",
        "",
        new_content,
        flags=re.DOTALL,
    )
    new_content = new_content.replace("<!-- agent-banner -->\n\n", "")
    return new_content


@app.command()
def generate_readme() -> None:
    """
    Generate README.md content from main index.md
    """
    typer.echo("Generating README")
    readme_path = Path("README.md")
    new_content = generate_readme_content()
    readme_path.write_text(new_content, encoding="utf-8")


@app.command()
def verify_readme() -> None:
    """
    Verify README.md content from main index.md
    """
    typer.echo("Verifying README")
    readme_path = Path("README.md")
    generated_content = generate_readme_content()
    readme_content = readme_path.read_text("utf-8")
    if generated_content != readme_content:
        typer.secho(
            "README.md outdated from the latest index.md", color=typer.colors.RED
        )
        raise typer.Abort()
    typer.echo("Valid README ✅")


@app.command()
def live(dirty: bool = False) -> None:
    """
    Serve with livereload a docs site for a specific language.

    This only shows the actual translated files, not the placeholders created with
    build-all.

    Takes an optional LANG argument with the name of the language to serve, by default
    en.
    """
    # Enable line numbers during local development to make it easier to highlight
    args = ["zensical", "serve", "--dev-addr", "127.0.0.1:8008"]
    if dirty:
        args.append("--dirty")
    subprocess.run(args, env={**os.environ, "LINENUMS": "true"}, check=True)


@app.command()
def build() -> None:
    """
    Build the docs.
    """
    print("Building docs")
    subprocess.run(["zensical", "build"], check=True)
    typer.secho("Successfully built docs", color=typer.colors.GREEN)


@app.command()
def serve() -> None:
    """
    A quick server to preview a built site.

    For development, prefer the command live (or just zensical serve).

    This is here only to preview the documentation site.

    Make sure you run the build command first.
    """
    typer.echo("Warning: this is a very simple server.")
    typer.echo("For development, use the command live instead.")
    typer.echo("This is here only to preview the documentation site.")
    typer.echo("Make sure you run the build command first.")
    os.chdir("site")
    server_address = ("", 8008)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    typer.echo("Serving at: http://127.0.0.1:8008")
    server.serve_forever()


@app.command()
def remove_unused_docs_src() -> None:
    """
    Delete unused Python snippets, keeping their variants and supporting package files.
    """
    docs_src_path = Path("docs_src")
    all_docs_content = "\n".join(
        md_file.read_text(encoding="utf-8") for md_file in docs_path.rglob("*.md")
    )
    variant_suffix = re.compile(r"(?:_non_an|_an)?(?:_py\d+)?$")

    def variant_key(path: Path) -> tuple[str, ...]:
        return tuple(variant_suffix.sub("", part, count=1) for part in path.parts)

    def package_key(parts: tuple[str, ...]) -> tuple[str, ...] | None:
        # Package examples use app, app02, or tutorial001 directories.
        for index, part in enumerate(parts):
            if re.fullmatch(r"(?:app\d*|tutorial\d+\w*)", part):
                return parts[: index + 1]
        return None

    file_keys = {
        py_file: variant_key(py_file.relative_to(docs_src_path).with_suffix(""))
        for py_file in docs_src_path.rglob("*.py")
    }
    used_files = {
        key
        for py_file, key in file_keys.items()
        if py_file.as_posix() in all_docs_content
    }
    # Keep entire referenced packages, including their variants and modules
    # imported by the referenced file, without keeping unrelated tutorial packages.
    used_package_dirs = {
        package for key in used_files if (package := package_key(key[:-1])) is not None
    }
    removed = 0
    for py_file, key in sorted(file_keys.items()):
        if py_file.name == "__init__.py" or key in used_files:
            continue
        if package_key(key[:-1]) in used_package_dirs:
            continue
        logging.info(f"Removing unused file: {py_file}")
        py_file.unlink()
        removed += 1
    # Preserve init-only subpackages inside used packages, and clean up unused ones.
    for dir_path in sorted(docs_src_path.rglob("*"), reverse=True):
        if not dir_path.is_dir():
            continue
        key = variant_key(dir_path.relative_to(docs_src_path))
        if package_key(key) in used_package_dirs:
            continue
        remaining = [
            f
            for f in dir_path.iterdir()
            if f.name != "__pycache__" and f.name != "__init__.py"
        ]
        if not remaining:
            logging.info(f"Removing empty/init-only directory: {dir_path}")
            shutil.rmtree(dir_path)
    print(f"Removed {removed} unused file(s) ✅")


if __name__ == "__main__":
    app()
