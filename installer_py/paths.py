"""Path handling and validation utilities."""

import os
from pathlib import Path
from typing import Optional


def normalize_path(path: str) -> str:
    """Normalize a path (expand ~, resolve ., convert backslashes)."""
    # Expand tilde
    expanded = os.path.expanduser(path)
    # Convert backslashes to forward slashes (Windows compatibility)
    normalized = expanded.replace("\\", "/")
    # Remove trailing slashes
    normalized = normalized.rstrip("/")
    # Make absolute if relative
    if not os.path.isabs(normalized):
        normalized = os.path.abspath(normalized)
    return normalized


def validate_install_path(path: str) -> tuple[bool, Optional[str]]:
    """
    Validate that a path is suitable for installation.

    Returns:
        (is_valid, error_message)
    """
    path_obj = Path(path)
    parent = path_obj.parent

    # Check if parent directory exists
    if not parent.exists():
        return False, f"Parent directory does not exist: {parent}"

    # Check if parent is writable
    if not os.access(parent, os.W_OK):
        return False, f"No write permission for directory: {parent}"

    # If target exists, check if writable
    if path_obj.exists() and not os.access(path, os.W_OK):
        return False, f"No write permission for directory: {path}"

    return True, None


def get_install_path(registry_path: str, install_dir: str) -> str:
    """
    Convert a registry path to an installation path.

    Registry paths are like ".opencode/agent/foo.md"
    We strip .opencode/ and prepend install_dir
    """
    # Strip leading .opencode/ if present
    if registry_path.startswith(".opencode/"):
        relative_path = registry_path[len(".opencode/") :]
    else:
        relative_path = registry_path

    # Return install_dir + relative path
    return os.path.join(install_dir, relative_path)


def ensure_parent_dir(file_path: str) -> None:
    """Ensure the parent directory of a file exists."""
    parent = Path(file_path).parent
    parent.mkdir(parents=True, exist_ok=True)
