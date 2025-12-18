"""Registry loading and parsing."""

import json
from pathlib import Path
from typing import Dict, List, Optional
import shutil

from .types import Component, ComponentType, Profile
from .network import fetch_url


def get_registry_key(comp_type: ComponentType) -> str:
    """Get the registry key for a component type (handles singular/plural)."""
    if comp_type == ComponentType.CONFIG:
        return "config"
    else:
        return f"{comp_type.value}s"


def load_registry(
    registry_path: Path,
    use_local: bool = False,
    local_path: Optional[Path] = None,
    registry_url: Optional[str] = None,
) -> Optional[Dict]:
    """
    Load the registry from local file or remote URL.

    Args:
        registry_path: Where to save/load the registry
        use_local: Whether to use a local file
        local_path: Path to local registry file (if use_local is True)
        registry_url: URL to fetch registry from (if use_local is False)

    Returns:
        Parsed registry dict or None if failed
    """
    if use_local:
        # Use local registry
        source_path = local_path or Path("registry.json")
        if not source_path.exists():
            return None

        # Copy to temp location
        shutil.copy(source_path, registry_path)
    else:
        # Fetch from remote URL
        if not registry_url:
            return None

        if not fetch_url(registry_url, registry_path):
            return None

    # Parse the registry
    try:
        with open(registry_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def parse_components(registry: Dict) -> Dict[ComponentType, List[Component]]:
    """Parse components from registry into structured format."""
    result = {}

    for comp_type in ComponentType:
        registry_key = get_registry_key(comp_type)
        components_data = registry.get("components", {}).get(registry_key, [])

        components = []
        for comp_data in components_data:
            comp = Component.from_dict(comp_data, comp_type)
            components.append(comp)

        result[comp_type] = components

    return result


def parse_profiles(registry: Dict) -> Dict[str, Profile]:
    """Parse profiles from registry."""
    profiles = {}

    profiles_data = registry.get("profiles", {})
    for profile_id, profile_data in profiles_data.items():
        profile = Profile(
            id=profile_id,
            name=profile_data.get("name", profile_id),
            description=profile_data.get("description", ""),
            components=profile_data.get("components", []),
            badge=profile_data.get("badge"),
            additional_paths=profile_data.get("additionalPaths", []),
        )
        profiles[profile_id] = profile

    return profiles


def find_component(
    components: Dict[ComponentType, List[Component]], component_id: str
) -> Optional[Component]:
    """Find a component by its full ID (type:id)."""
    if ":" not in component_id:
        return None

    type_str, comp_id = component_id.split(":", 1)

    # Map type string to ComponentType
    try:
        if type_str == "agent":
            comp_type = ComponentType.AGENT
        elif type_str == "subagent":
            comp_type = ComponentType.SUBAGENT
        elif type_str == "command":
            comp_type = ComponentType.COMMAND
        elif type_str == "tool":
            comp_type = ComponentType.TOOL
        elif type_str == "plugin":
            comp_type = ComponentType.PLUGIN
        elif type_str == "context":
            comp_type = ComponentType.CONTEXT
        elif type_str == "config":
            comp_type = ComponentType.CONFIG
        else:
            return None
    except:
        return None

    # Find the component
    for comp in components.get(comp_type, []):
        if comp.id == comp_id:
            return comp

    return None
