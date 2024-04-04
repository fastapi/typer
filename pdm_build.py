import os
from typing import Any, Dict, List

from pdm.backend.hooks import Context

TIANGOLO_BUILD_PACKAGE = os.getenv("TIANGOLO_BUILD_PACKAGE", "typer")


def pdm_build_initialize(context: Context):
    metadata = context.config.metadata
    # Get main version
    version = metadata["version"]
    sync_dependencies: List[str] = context.config.data["tool"]["tiangolo"][
        "_internal_slim_build"
    ]["sync_dependencies"]
    config: Dict[str, Any] = context.config.data["tool"]["tiangolo"][
        "_internal_slim_build"
    ]["packages"][TIANGOLO_BUILD_PACKAGE]
    project_config: Dict[str, Any] = config["project"]
    for key, value in project_config.items():
        metadata[key] = value
    build_config: Dict[str, Any] = (
        config.get("tool", {}).get("pdm", {}).get("build", {})
    )
    for key, value in build_config.items():
        context.config.build_config[key] = value
    dependencies: List[str] = metadata.get("dependencies", [])
    new_dependencies = []
    for dep in dependencies:
        if dep in sync_dependencies:
            new_dep = f"{dep}=={version}"
            new_dependencies.append(new_dep)
        else:
            new_dependencies.append(dep)
    if new_dependencies != dependencies:
        metadata["dependencies"] = new_dependencies
