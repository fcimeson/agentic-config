"""Component selection and interactive menus."""

from __future__ import annotations

from typing import Dict, List

from .console import get_console, Colors
from .types import Component, ComponentType, Profile


console = get_console()


def show_profile_menu(profiles: Dict[str, Profile]) -> str:
    """Show interactive profile selection menu."""
    console.print_header()
    console.print(console.color("Choose installation profile:\n", Colors.BOLD))

    profile_items = list(profiles.items())

    for idx, (profile_id, profile) in enumerate(profile_items, 1):
        badge = (
            f" {console.color(f'[{profile.badge}]', Colors.GREEN)}"
            if profile.badge
            else ""
        )
        color = [Colors.GREEN, Colors.BLUE, Colors.CYAN, Colors.MAGENTA, Colors.YELLOW][
            (idx - 1) % 5
        ]
        console.print(f"  {console.color(f'{idx})', color)} {profile.name}{badge}")
        console.print(f"     {profile.description}")
        console.print(f"     Components: {len(profile.components)}\n")

    console.print(f"  {len(profile_items) + 1}) Back to main menu\n")

    try:
        choice = input("Enter your choice: ").strip()
        choice_num = int(choice)
        if 1 <= choice_num <= len(profile_items):
            return profile_items[choice_num - 1][0]
        return ""
    except (ValueError, KeyboardInterrupt):
        return ""


def show_main_menu() -> str:
    """Show main installation mode menu."""
    console.print_header()
    console.print(console.color("Choose installation mode:\n", Colors.BOLD))
    console.print("  1) Quick Install (Choose a profile)")
    console.print("  2) Custom Install (Pick individual components)")
    console.print("  3) List Available Components")
    console.print("  4) Exit\n")

    try:
        choice = input("Enter your choice [1-4]: ").strip()
        return {
            "1": "profile",
            "2": "custom",
            "3": "list",
            "4": "exit",
        }.get(choice, show_main_menu())
    except KeyboardInterrupt:
        return "exit"


def show_install_location_menu(current_dir: str, global_path: str) -> str:
    """Show installation location selection menu."""
    console.print_header()
    console.print(console.color("Choose installation location:", Colors.BOLD))
    console.print(
        f"  {console.color('1) Local', Colors.GREEN)} - Install to {console.color('.opencode/', Colors.CYAN)}"
    )
    console.print("     (Best for project-specific agents)\n")
    console.print(
        f"  {console.color('2) Global', Colors.BLUE)} - Install to {console.color(global_path, Colors.CYAN)}"
    )
    console.print("     (Best for user-wide agents)\n")
    console.print(f"  {console.color('3) Custom', Colors.MAGENTA)} - Enter exact path")
    console.print("     Examples: ~/my-agents\n")
    console.print("  4) Back / Exit\n")

    try:
        choice = input("Enter your choice [1-4]: ").strip()
        if choice == "1":
            return ".opencode"
        if choice == "2":
            return global_path
        if choice == "3":
            custom = input("\nEnter installation path: ").strip()
            return custom or ".opencode"
        if choice == "4":
            raise SystemExit(0)
        console.print_error("Invalid choice")
        return show_install_location_menu(current_dir, global_path)
    except KeyboardInterrupt:
        raise SystemExit(0)


def list_all_components(components: Dict[ComponentType, List[Component]]) -> None:
    """Display all available components."""
    console.print_header()
    console.print(console.color("Available Components\n", Colors.BOLD))

    for comp_type in ComponentType:
        comps = components.get(comp_type, [])
        if not comps:
            continue
        type_name = comp_type.value.capitalize()
        console.print(console.color(f"{type_name}s:", Colors.CYAN + Colors.BOLD))
        for comp in comps:
            console.print(f"  {console.color(comp.name, Colors.GREEN)} ({comp.id})")
            console.print(f"    {comp.description}")
        console.print()
    input("Press Enter to continue...")
