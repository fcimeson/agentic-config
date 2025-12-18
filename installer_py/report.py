"""Installation report and post-install messaging."""

from typing import Optional, List
from .types import InstallResult
from .console import print_success, print_step, print_info, colorize, Colors


def show_installation_summary(
    result: InstallResult,
    install_dir: str,
    profile: Optional[str] = None,
    component_count: int = 0,
) -> None:
    """Show installation summary with counts."""
    print()
    print_success("Installation complete!")
    print(f"  Installed: {colorize(str(result.installed), Colors.GREEN)}")

    if result.skipped > 0:
        print(f"  Skipped: {colorize(str(result.skipped), Colors.CYAN)}")

    if result.failed > 0:
        print(f"  Failed: {colorize(str(result.failed), Colors.RED)}")

    if result.backup_dir:
        print(f"  Backup: {colorize(result.backup_dir, Colors.CYAN)}")


def show_post_install(install_dir: str, repo_url: str) -> None:
    """Show post-installation instructions."""
    print()
    print_step("Next Steps")

    print(f"1. Review the installed components in {colorize(install_dir, Colors.CYAN)}")
    print(f"2. Start using OpenCode agents:")
    print(f"   {colorize('opencode --agent openagent', Colors.CYAN)}")
    print()

    print_info(f"Installation directory: {colorize(install_dir, Colors.CYAN)}")
    print_info(f"Documentation: {repo_url}")
    print()


def show_installation_preview(
    component_ids: List[str], install_dir: str, profile: Optional[str] = None
) -> None:
    """Show installation preview before proceeding."""
    print(f"\n{colorize('Installation Preview', Colors.BOLD)}\n")

    if profile:
        print(f"Profile: {colorize(profile, Colors.GREEN)}")
    else:
        print(f"Mode: {colorize('Custom', Colors.GREEN)}")

    print(f"Installation directory: {colorize(install_dir, Colors.CYAN)}")
    print(f"\nComponents to install ({len(component_ids)} total):\n")

    # Group by type
    groups = {}
    for comp_id in component_ids:
        comp_type = comp_id.split(":")[0] if ":" in comp_id else "unknown"
        if comp_type not in groups:
            groups[comp_type] = []
        groups[comp_type].append(comp_id.split(":")[1] if ":" in comp_id else comp_id)

    # Display grouped components
    for comp_type, ids in sorted(groups.items()):
        type_name = comp_type.capitalize() + "s"
        ids_str = ", ".join(ids)
        print(f"{colorize(f'{type_name} ({len(ids)}):', Colors.CYAN)} {ids_str}")

    print()
