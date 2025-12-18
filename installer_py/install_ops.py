"""Installation operations (file copying, downloading, etc)."""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional

from .types import Component, ComponentType, CollisionStrategy, InstallResult
from .network import fetch_url
from .paths import get_install_path, ensure_parent_dir
from .transform import transform_context_paths, should_transform
from .console import print_success, print_error, print_info, print_step
from .registry import find_component


def install_components(
    component_ids: List[str],
    components_dict: Dict[ComponentType, List[Component]],
    install_dir: str,
    raw_url: str,
    use_local_files: bool,
    local_base_path: Path,
    collision_strategy: CollisionStrategy,
) -> InstallResult:
    """
    Install a list of components.

    Args:
        component_ids: List of component IDs to install (type:id format)
        components_dict: Dictionary of all available components
        install_dir: Installation directory
        raw_url: Base URL for downloading files
        use_local_files: Whether to copy from local files
        local_base_path: Base path for local files
        collision_strategy: How to handle existing files

    Returns:
        InstallResult with counts and errors
    """
    print_step("Installing components...")

    result = InstallResult()

    # Ensure base directory exists
    Path(install_dir).mkdir(parents=True, exist_ok=True)

    for comp_id in component_ids:
        comp = find_component(components_dict, comp_id)
        if not comp:
            result.errors.append(f"Component not found: {comp_id}")
            result.failed += 1
            continue

        if not comp.path or comp.path == "null":
            result.errors.append(f"No path for component: {comp_id}")
            result.failed += 1
            continue

        # Get installation path
        dest_path = get_install_path(comp.path, install_dir)

        # Check if file exists
        file_existed = os.path.exists(dest_path)

        # Handle collision strategy
        if file_existed and collision_strategy == CollisionStrategy.SKIP:
            print_info(f"Skipped existing: {comp.type.value}:{comp.id}")
            result.skipped += 1
            continue

        # Ensure parent directory exists
        ensure_parent_dir(dest_path)

        # Install the file
        success = False
        if use_local_files:
            # Copy from local file
            src_path = local_base_path / comp.path
            if not src_path.exists():
                print_error(
                    f"Local source not found for {comp.type.value}:{comp.id}: {src_path}"
                )
                result.failed += 1
                continue

            try:
                shutil.copy2(src_path, dest_path)
                success = True
            except Exception as e:
                print_error(f"Failed to copy {comp.type.value}:{comp.id}: {e}")
                result.failed += 1
                continue
        else:
            # Download from remote URL
            file_url = f"{raw_url}/{comp.path}"
            success = fetch_url(file_url, Path(dest_path))

            if not success:
                print_error(f"Failed to download {comp.type.value}:{comp.id}")
                result.failed += 1
                continue

        # Transform paths if needed
        if success and should_transform(install_dir):
            try:
                with open(dest_path, "r", encoding="utf-8") as f:
                    content = f.read()

                transformed = transform_context_paths(content, install_dir)

                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(transformed)
            except Exception:
                # If transformation fails, that's okay - file is still installed
                pass

        # Report success
        if file_existed:
            print_success(f"Updated {comp.type.value}: {comp.id}")
        else:
            print_success(f"Installed {comp.type.value}: {comp.id}")

        result.installed += 1

    return result
