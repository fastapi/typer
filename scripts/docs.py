import logging
import os
import re
import shutil
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import typer
from ruff.__main__ import find_ruff_bin

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
    args = ["mkdocs", "serve", "--dev-addr", "127.0.0.1:8008"]
    if dirty:
        args.append("--dirty")
    subprocess.run(args, env={**os.environ, "LINENUMS": "true"}, check=True)


@app.command()
def build() -> None:
    """
    Build the docs.
    """
    print("Building docs")
    subprocess.run(["mkdocs", "build"], check=True)
    typer.secho("Successfully built docs", color=typer.colors.GREEN)


@app.command()
def serve() -> None:
    """
    A quick server to preview a built site.

    For development, prefer the command live (or just mkdocs serve).

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
def generate_docs_src_versions_for_file(file_path: Path) -> None:
    target_versions = ["py39", "py310"]
    full_path_str = str(file_path)
    for target_version in target_versions:
        if f"_{target_version}" in full_path_str:
            logging.info(
                f"Skipping {file_path}, already a version file for {target_version}"
            )
            return
    base_content = file_path.read_text(encoding="utf-8")
    previous_content = {base_content}
    for target_version in target_versions:
        version_result = subprocess.run(
            [
                find_ruff_bin(),
                "check",
                "--target-version",
                target_version,
                "--fix",
                "--unsafe-fixes",
                "-",
            ],
            input=base_content.encode("utf-8"),
            capture_output=True,
        )
        content_target = version_result.stdout.decode("utf-8")
        format_result = subprocess.run(
            [find_ruff_bin(), "format", "-"],
            input=content_target.encode("utf-8"),
            capture_output=True,
        )
        content_format = format_result.stdout.decode("utf-8")
        if content_format in previous_content:
            continue
        previous_content.add(content_format)
        # Determine where the version label should go: in the parent directory
        # name or in the file name, matching the source structure.
        label_in_parent = False
        for v in target_versions:
            if f"_{v}" in file_path.parent.name:
                label_in_parent = True
                break
        if label_in_parent:
            parent_name = file_path.parent.name
            for v in target_versions:
                parent_name = parent_name.replace(f"_{v}", "")
            new_parent = file_path.parent.parent / f"{parent_name}_{target_version}"
            new_parent.mkdir(parents=True, exist_ok=True)
            version_file = new_parent / file_path.name
        else:
            base_name = file_path.stem
            for v in target_versions:
                if base_name.endswith(f"_{v}"):
                    base_name = base_name[: -len(f"_{v}")]
                    break
            version_file = file_path.with_name(f"{base_name}_{target_version}.py")
        logging.info(f"Writing to {version_file}")
        version_file.write_text(content_format, encoding="utf-8")


@app.command()
def generate_docs_src_versions() -> None:
    """
    Generate Python version-specific files for all .py files in docs_src.
    """
    docs_src_path = Path("docs_src")
    for py_file in sorted(docs_src_path.rglob("*.py")):
        generate_docs_src_versions_for_file(py_file)


@app.command()
def copy_py39_to_py310() -> None:
    """
    For each docs_src file/directory with a _py39 label that has no _py310
    counterpart, copy it with the _py310 label.
    """
    docs_src_path = Path("docs_src")
    # Handle directory-level labels (e.g. app_b_an_py39/)
    for dir_path in sorted(docs_src_path.rglob("*_py39")):
        if not dir_path.is_dir():
            continue
        py310_dir = dir_path.parent / dir_path.name.replace("_py39", "_py310")
        if py310_dir.exists():
            continue
        logging.info(f"Copying directory {dir_path} -> {py310_dir}")
        shutil.copytree(dir_path, py310_dir)
    # Handle file-level labels (e.g. tutorial001_py39.py)
    for file_path in sorted(docs_src_path.rglob("*_py39.py")):
        if not file_path.is_file():
            continue
        # Skip files inside _py39 directories (already handled above)
        if "_py39" in file_path.parent.name:
            continue
        py310_file = file_path.with_name(
            file_path.name.replace("_py39.py", "_py310.py")
        )
        if py310_file.exists():
            continue
        logging.info(f"Copying file {file_path} -> {py310_file}")
        shutil.copy2(file_path, py310_file)


@app.command()
def update_docs_includes_py39_to_py310() -> None:
    """
    Update .md files in docs/en/ to replace _py39 includes with _py310 versions.

    For each include line referencing a _py39 file or directory in docs_src, replace
    the _py39 label with _py310.
    """
    include_pattern = re.compile(r"\{[^}]*docs_src/[^}]*_py39[^}]*\.py[^}]*\}")
    count = 0
    for md_file in sorted(en_docs_path.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if "_py39" not in content:
            continue
        new_content = include_pattern.sub(
            lambda m: m.group(0).replace("_py39", "_py310"), content
        )
        if new_content != content:
            md_file.write_text(new_content, encoding="utf-8")
            count += 1
            logging.info(f"Updated includes in {md_file}")
    print(f"Updated {count} file(s) ✅")


@app.command()
def remove_unused_docs_src() -> None:
    """
    Delete .py files in docs_src that are not included in any .md file under docs/.
    """
    docs_src_path = Path("docs_src")
    # Collect all docs .md content referencing docs_src
    all_docs_content = ""
    for md_file in docs_path.rglob("*.md"):
        all_docs_content += md_file.read_text(encoding="utf-8")
    # Build a set of directory-based package roots (e.g. docs_src/bigger_applications/app_py39)
    # where at least one file is referenced in docs. All files in these directories
    # should be kept since they may be internally imported by the referenced files.
    used_package_dirs: set[Path] = set()
    for py_file in docs_src_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        rel_path = str(py_file)
        if rel_path in all_docs_content:
            # Walk up from the file's parent to find the package root
            # (a subdirectory under docs_src/<topic>/)
            parts = py_file.relative_to(docs_src_path).parts
            if len(parts) > 2 and not py_file.name.startswith("tutorial"):
                # File is inside a sub-package like docs_src/topic/app_xxx/...
                # but not a standalone tutorial file in a topic subdirectory
                package_root = docs_src_path / parts[0] / parts[1]
                used_package_dirs.add(package_root)
    removed = 0
    for py_file in sorted(docs_src_path.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        # Build the relative path as it appears in includes (e.g. docs_src/first_steps/tutorial001.py)
        rel_path = str(py_file)
        if rel_path in all_docs_content:
            continue
        # If this file is inside a directory-based package where any sibling is
        # referenced, keep it (it's likely imported internally).
        parts = py_file.relative_to(docs_src_path).parts
        if len(parts) > 2:
            package_root = docs_src_path / parts[0] / parts[1]
            if package_root in used_package_dirs:
                continue
        # Check if the _an counterpart (or non-_an counterpart) is referenced.
        # If either variant is included, keep both.
        # Handle both file-level _an (tutorial001_an.py) and directory-level _an
        # (app_an/main.py)
        counterpart_found = False
        full_path_str = str(py_file)
        if "_an" in py_file.stem:
            # This is an _an file, check if the non-_an version is referenced
            counterpart = full_path_str.replace(
                f"/{py_file.stem}", f"/{py_file.stem.replace('_an', '', 1)}"
            )
            if counterpart in all_docs_content:
                counterpart_found = True
        else:
            # This is a non-_an file, check if there's an _an version referenced
            # Insert _an before any version suffix or at the end of the stem
            stem = py_file.stem
            for suffix in ("_py39", "_py310"):
                if suffix in stem:
                    an_stem = stem.replace(suffix, f"_an{suffix}", 1)
                    break
            else:
                an_stem = f"{stem}_an"
            counterpart = full_path_str.replace(f"/{stem}.", f"/{an_stem}.")
            if counterpart in all_docs_content:
                counterpart_found = True
        # Also check directory-level _an counterparts
        if not counterpart_found:
            parent_name = py_file.parent.name
            if "_an" in parent_name:
                counterpart_parent = parent_name.replace("_an", "", 1)
                counterpart_dir = str(py_file).replace(
                    f"/{parent_name}/", f"/{counterpart_parent}/"
                )
                if counterpart_dir in all_docs_content:
                    counterpart_found = True
            else:
                # Try inserting _an into parent directory name
                for suffix in ("_py39", "_py310"):
                    if suffix in parent_name:
                        an_parent = parent_name.replace(suffix, f"_an{suffix}", 1)
                        break
                else:
                    an_parent = f"{parent_name}_an"
                counterpart_dir = str(py_file).replace(
                    f"/{parent_name}/", f"/{an_parent}/"
                )
                if counterpart_dir in all_docs_content:
                    counterpart_found = True
        if counterpart_found:
            continue
        logging.info(f"Removing unused file: {py_file}")
        py_file.unlink()
        removed += 1
    # Clean up directories that are empty or only contain __init__.py / __pycache__
    for dir_path in sorted(docs_src_path.rglob("*"), reverse=True):
        if not dir_path.is_dir():
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
