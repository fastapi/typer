import os
from typing import List

from pdm.backend.hooks import Context

packages_to_sync = ["typer-slim", "typer-cli"]

TYPER_SLIM_BUILD = os.getenv("TYPER_SLIM_BUILD")


def pdm_build_hook_enabled(context: Context):
    return context.target == "sdist"


def pdm_build_initialize(context: Context):
    metadata = context.config.metadata
    # Get main version
    version = metadata["version"]
    if TYPER_SLIM_BUILD:
        metadata["name"] = "typer-slim"
    else:
        typer_config_data = context.config.data["tool"]["typer"]["_internal_build"]
        typer_dependencies: List[str] = typer_config_data["dependencies"]

        new_dependencies = []
        for dep in typer_dependencies:
            if any(dep.startswith(name) for name in packages_to_sync):
                new_dep = f"{dep}=={version}"
                new_dependencies.append(new_dep)
            else:
                new_dependencies.append(dep)
        if new_dependencies != typer_dependencies:
            metadata["dependencies"] = new_dependencies
        metadata["optional-dependencies"] = {}
