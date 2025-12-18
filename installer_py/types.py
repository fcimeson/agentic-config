"""Type definitions for the installer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .config import InstallerConfig


class ComponentType(Enum):
    """Component types available in the registry."""

    AGENT = "agent"
    SUBAGENT = "subagent"
    COMMAND = "command"
    TOOL = "tool"
    PLUGIN = "plugin"
    CONTEXT = "context"
    CONFIG = "config"


class CollisionStrategy(Enum):
    """Strategies for handling file collisions."""

    FRESH = "fresh"
    SKIP = "skip"
    OVERWRITE = "overwrite"
    BACKUP = "backup"
    CANCEL = "cancel"


@dataclass
class Component:
    """Represents a component from the registry."""

    id: str
    name: str
    type: ComponentType
    path: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    category: str = "standard"

    @staticmethod
    def from_dict(data: Dict[str, Any], comp_type: ComponentType) -> "Component":
        """Create a Component from dictionary data."""
        return Component(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=comp_type,
            path=data.get("path", ""),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            dependencies=data.get("dependencies", []),
            category=data.get("category", "standard"),
        )


@dataclass
class Profile:
    """Represents an installation profile."""

    id: str
    name: str
    description: str
    components: List[str]
    badge: Optional[str] = None
    additional_paths: List[str] = field(default_factory=list)


@dataclass
class InstallResult:
    """Result of an installation operation."""

    installed: int = 0
    skipped: int = 0
    failed: int = 0
    backup_dir: Optional[str] = None
    errors: List[str] = field(default_factory=list)


ComponentMap = Dict[ComponentType, List[Component]]
ProfileMap = Dict[str, Profile]


@dataclass
class RegistryData:
    components: ComponentMap
    profiles: ProfileMap
    raw: Dict[str, Any]


@dataclass
class InstallContext:
    config: "InstallerConfig"
    registry: RegistryData
    selected_components: List[str]
    profile: Optional[str]
    collision_strategy: CollisionStrategy = CollisionStrategy.FRESH
    backup_dir: Optional[Path] = None
    non_interactive: bool = False


__all__ = [
    "Component",
    "ComponentType",
    "Profile",
    "InstallResult",
    "ComponentMap",
    "ProfileMap",
    "CollisionStrategy",
    "RegistryData",
    "InstallContext",
]
