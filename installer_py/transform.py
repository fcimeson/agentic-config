"""Path transformation utilities for global installs."""

import os
import re


def transform_context_paths(content: str, install_dir: str) -> str:
    """
    Transform @.opencode/context/ references to the actual install path.

    Only transforms if installing to a non-local path.
    Local paths are .opencode or */.opencode
    """
    # Check if this is a local install
    normalized_dir = install_dir.replace("\\", "/")
    if normalized_dir.endswith("/.opencode") or normalized_dir == ".opencode":
        # Don't transform for local installs
        return content

    # Expand tilde for transformations
    expanded_path = os.path.expanduser(install_dir)

    # Transform @.opencode/context/ to @{install_dir}/context/
    content = re.sub(r"@\.opencode/context/", f"@{expanded_path}/context/", content)

    # Transform .opencode/context to {install_dir}/context (without @)
    content = re.sub(r"\.opencode/context", f"{expanded_path}/context", content)

    return content


def should_transform(install_dir: str) -> bool:
    """Check if path transformations should be applied."""
    normalized_dir = install_dir.replace("\\", "/")
    return not (normalized_dir.endswith("/.opencode") or normalized_dir == ".opencode")
