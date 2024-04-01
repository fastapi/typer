from pathlib import Path
from typing import List

from pdm.backend.hooks import Context

packages_to_sync = ["typer-slim", "typer-cli"]

readme_name = "README.md"
license_name = "LICENSE"
readme_path = Path("..") / readme_name
license_path = Path("..") / license_name


def pdm_build_hook_enabled(context: Context):
    return context.target == "sdist"


def pdm_build_initialize(context: Context):
    metadata = context.config.metadata
    # Get main version
    version = metadata["version"]
    # Update version in dependencies to sync them
    dependencies: List[str] = metadata["dependencies"]
    new_dependencies = []
    for dep in dependencies:
        if any(dep.startswith(name) for name in packages_to_sync):
            new_dep = f"{dep}=={version}"
            new_dependencies.append(new_dep)
        else:
            new_dependencies.append(dep)
    if new_dependencies != dependencies:
        metadata["dependencies"] = new_dependencies
    # README.md and LICENSE
    readme_content = readme_path.read_text()
    license_content = license_path.read_text()
    metadata["readme"] = readme_name
    context.ensure_build_dir()
    # Copy README.md and LICENSE to build directory
    # (context.build_dir / readme_name).write_text(readme_content)
    # (context.build_dir / license_name).write_text(license_content)
    # # Workaround, copy README.md and LICENSE to package_dir during build
    Path(readme_name).write_text(readme_content)
    Path(license_name).write_text(license_content)


def pdm_build_finalize(context: Context, artifact: Path):
    # Workaround, remove README.md and LICENSE from package_dir after build
    Path(readme_name).unlink()
    Path(license_name).unlink()
