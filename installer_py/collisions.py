"""Collision detection and handling."""

import os
from pathlib import Path
from typing import List, Dict, Optional
from .types import CollisionStrategy, ComponentType
from .console import print_warning, print_info, colorize, Colors


def detect_collisions(component_paths: List[str], install_dir: str) -> List[str]:
    """
    Detect which files already exist at installation paths.

    Returns:
        List of paths that already exist
    """
    collisions = []

    for path in component_paths:
        if os.path.exists(path):
            collisions.append(path)

    return collisions


def show_collision_report(collisions: List[str]) -> None:
    """Display collision report grouped by type."""
    print()
    print_warning(f"Found {len(collisions)} file collision(s):")
    print()

    # Group by type
    groups = {
        "agents": [],
        "subagents": [],
        "commands": [],
        "tools": [],
        "plugins": [],
        "contexts": [],
        "configs": [],
    }

    for file_path in collisions:
        if "/agent/subagents/" in file_path:
            groups["subagents"].append(file_path)
        elif "/agent/" in file_path:
            groups["agents"].append(file_path)
        elif "/command/" in file_path:
            groups["commands"].append(file_path)
        elif "/tool/" in file_path:
            groups["tools"].append(file_path)
        elif "/plugin/" in file_path:
            groups["plugins"].append(file_path)
        elif "/context/" in file_path:
            groups["contexts"].append(file_path)
        else:
            groups["configs"].append(file_path)

    # Display grouped collisions
    for group_name, files in groups.items():
        if files:
            print(
                f"{colorize(f'  {group_name.capitalize()} ({len(files)}):', Colors.YELLOW)}"
            )
            for f in files:
                print(f"    {f}")

    print()


def get_collision_strategy() -> CollisionStrategy:
    """
    Prompt user for collision handling strategy.

    Returns:
        Selected CollisionStrategy
    """
    print(f"{colorize('How would you like to proceed?', Colors.BOLD)}\n")
    print(
        f"  1) {colorize('Skip existing', Colors.GREEN)} - Only install new files, keep all existing files unchanged"
    )
    print(
        f"  2) {colorize('Overwrite all', Colors.YELLOW)} - Replace existing files with new versions (your changes will be lost)"
    )
    print(
        f"  3) {colorize('Backup & overwrite', Colors.CYAN)} - Backup existing files, then install new versions"
    )
    print(f"  4) {colorize('Cancel', Colors.RED)} - Exit without making changes")
    print()

    try:
        choice = input("Enter your choice [1-4]: ").strip()

        if choice == "1":
            return CollisionStrategy.SKIP
        elif choice == "2":
            # Confirm overwrite
            print()
            print_warning(
                "This will overwrite existing files. Your changes will be lost!"
            )
            confirm = input("Are you sure? Type 'yes' to confirm: ").strip()
            if confirm.lower() == "yes":
                return CollisionStrategy.OVERWRITE
            else:
                return CollisionStrategy.CANCEL
        elif choice == "3":
            return CollisionStrategy.BACKUP
        elif choice == "4":
            return CollisionStrategy.CANCEL
        else:
            return CollisionStrategy.CANCEL
    except KeyboardInterrupt:
        return CollisionStrategy.CANCEL


def create_backup(files: List[str], install_dir: str) -> Optional[str]:
    """
    Create backup of files.

    Returns:
        Path to backup directory or None if no files were backed up
    """
    from datetime import datetime
    import shutil

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = f"{install_dir}.backup.{timestamp}"

    backup_count = 0
    for file_path in files:
        if os.path.exists(file_path):
            # Calculate relative path from install_dir
            try:
                rel_path = os.path.relpath(file_path, install_dir)
                backup_path = os.path.join(backup_dir, rel_path)

                # Ensure parent directory exists
                Path(backup_path).parent.mkdir(parents=True, exist_ok=True)

                # Copy the file
                shutil.copy2(file_path, backup_path)
                backup_count += 1
            except Exception:
                print_warning(f"Failed to backup: {file_path}")

    return backup_dir if backup_count > 0 else None
