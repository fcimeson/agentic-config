"""Python-based installer for agentic-config components."""

__version__ = "1.0.0"

# Export all modules for convenient importing
from . import (
    cli,
    config,
    console,
    platform,
    paths,
    registry,
    network,
    deps,
    selection,
    collisions,
    install_ops,
    transform,
    report,
    types,
)

__all__ = [
    "cli",
    "config",
    "console",
    "platform",
    "paths",
    "registry",
    "network",
    "deps",
    "selection",
    "collisions",
    "install_ops",
    "transform",
    "report",
    "types",
]
