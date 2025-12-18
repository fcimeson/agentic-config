"""Dependency resolution utilities."""

from typing import Dict, List, Set, Optional
from .types import Component, ComponentType


def resolve_dependencies(
    component_ids: List[str], components: Dict[ComponentType, List[Component]]
) -> List[str]:
    """
    Resolve dependencies for a list of component IDs.

    Returns:
        List of component IDs including all dependencies (topologically sorted)
    """
    resolved = []
    visited = set()

    def visit(comp_id: str):
        if comp_id in visited:
            return
        visited.add(comp_id)

        # Find the component
        comp = _find_component(components, comp_id)
        if not comp:
            return

        # Visit dependencies first (depth-first)
        for dep_id in comp.dependencies:
            visit(dep_id)

        # Add this component
        if comp_id not in resolved:
            resolved.append(comp_id)

    # Visit each requested component
    for comp_id in component_ids:
        visit(comp_id)

    return resolved


def _find_component(
    components: Dict[ComponentType, List[Component]], component_id: str
) -> Optional[Component]:
    """Find a component by its full ID (type:id)."""
    if ":" not in component_id:
        return None

    type_str, comp_id = component_id.split(":", 1)

    # Map type string to ComponentType
    try:
        comp_type = {
            "agent": ComponentType.AGENT,
            "subagent": ComponentType.SUBAGENT,
            "command": ComponentType.COMMAND,
            "tool": ComponentType.TOOL,
            "plugin": ComponentType.PLUGIN,
            "context": ComponentType.CONTEXT,
            "config": ComponentType.CONFIG,
        }.get(type_str)

        if not comp_type:
            return None
    except:
        return None

    # Find the component
    for comp in components.get(comp_type, []):
        if comp.id == comp_id:
            return comp

    return None
