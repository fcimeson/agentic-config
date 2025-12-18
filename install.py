#!/usr/bin/env python3
"""
OpenCode Component Installer (Python Implementation)

This installer replaces the bash-based install.sh with a pure Python implementation
while maintaining full backward compatibility and feature parity.
"""

import sys
import os
from pathlib import Path

# Check Python version first
if sys.version_info < (3, 9):
    print(
        f"Error: Python 3.9+ required (you have {sys.version_info.major}.{sys.version_info.minor})"
    )
    print("Please upgrade Python or use the bash installer (install.sh)")
    sys.exit(1)

from installer_py import cli, config, console, platform, paths, registry, deps
from installer_py import selection, collisions, install_ops, report
from installer_py.types import CollisionStrategy


def main() -> int:
    """Main installer entry point."""

    # Parse command-line arguments
    args, parser = cli.parse_args()

    # Build configuration
    cfg = config.build_config(
        branch=None,  # Will use env var or default
        install_dir=args.install_dir,
        use_local_files=args.local_files is not None,
        local_registry_path=args.local_files if args.local_files else None,
        script_path=Path(__file__).parent,
    )

    # Check if we should show list
    if args.list:
        console.print_header()
        console.print_step("Fetching component registry...")

        # Load registry
        registry_path = cfg.temp_dir / "registry.json"
        reg_data = registry.load_registry(
            registry_path,
            use_local=cfg.use_local_files,
            local_path=cfg.local_registry_path,
            registry_url=cfg.registry_url,
        )

        if not reg_data:
            console.print_error("Failed to load registry")
            return 1

        components_dict = registry.parse_components(reg_data)
        selection.list_all_components(components_dict)
        return 0

    # Show header
    console.print_header()

    # Load registry
    console.print_step("Fetching component registry...")

    if cfg.use_local_files:
        console.print_info("Registry source: local")
        console.print_info(
            f"Registry path: {cfg.local_registry_path or 'registry.json'}"
        )
    else:
        console.print_info("Registry source: remote")
        console.print_info(f"Registry URL: {cfg.registry_url}")

    registry_path = cfg.temp_dir / "registry.json"
    reg_data = registry.load_registry(
        registry_path,
        use_local=cfg.use_local_files,
        local_path=cfg.local_registry_path,
        registry_url=cfg.registry_url,
    )

    if not reg_data:
        console.print_error("Failed to load registry")
        return 1

    console.print_success("Registry loaded successfully")

    # Parse components and profiles
    components_dict = registry.parse_components(reg_data)
    profiles_dict = registry.parse_profiles(reg_data)

    # Determine installation mode
    selected_profile = args.profile
    selected_components = []
    non_interactive = selected_profile is not None

    if non_interactive:
        # Non-interactive mode with profile
        if selected_profile not in profiles_dict:
            console.print_error(f"Unknown profile: {selected_profile}")
            return 1

        profile = profiles_dict[selected_profile]
        selected_components = profile.components

    else:
        # Interactive mode
        if not console.is_interactive():
            console.print_error("Interactive mode requires a terminal")
            print()
            print(
                "You're running in a pipe. For interactive mode, download the script first:"
            )
            print()
            print(f"{console.colorize('# Download and run', console.Colors.CYAN)}")
            print(
                f"curl -fsSL https://raw.githubusercontent.com/{cfg.repo_slug}/main/install.py -o install.py"
            )
            print(f"python install.py")
            print()
            print("Or use a profile directly:")
            print(f"python install.py developer")
            print()
            return 1

        # Show install location menu first
        global_path = platform.get_global_install_path()
        install_dir_str = selection.show_install_location_menu(
            str(cfg.install_dir), global_path
        )
        cfg.install_dir = Path(install_dir_str)

        # Show main menu
        mode = selection.show_main_menu()

        if mode == "exit":
            return 0
        elif mode == "list":
            selection.list_all_components(components_dict)
            return main()  # Return to main menu
        elif mode == "profile":
            selected_profile = selection.show_profile_menu(profiles_dict)
            if not selected_profile:
                return main()  # Back to main menu

            profile = profiles_dict[selected_profile]
            selected_components = profile.components
        else:
            console.print_error("Custom component selection not yet implemented")
            console.print_info(
                "Please use profile mode or re-run with a profile argument"
            )
            return 1

    # Resolve dependencies
    if selected_components:
        console.print_step("Resolving dependencies...")
        original_count = len(selected_components)
        selected_components = deps.resolve_dependencies(
            selected_components, components_dict
        )

        if len(selected_components) > original_count:
            console.print_info(
                f"Added {len(selected_components) - original_count} dependencies"
            )

    # Show installation preview
    if not non_interactive:
        report.show_installation_preview(
            selected_components, str(cfg.install_dir), selected_profile
        )

        try:
            confirm = input("Proceed with installation? [Y/n]: ").strip().lower()
            if confirm == "n":
                console.print_info("Installation cancelled")
                return 0
        except KeyboardInterrupt:
            console.print_info("\nInstallation cancelled")
            return 0
    else:
        # Non-interactive: show preview but don't ask
        report.show_installation_preview(
            selected_components, str(cfg.install_dir), selected_profile
        )
        console.print_info("Installing automatically (profile specified)...")

    # Detect collisions
    console.print_step("Checking for file collisions...")

    # Get all destination paths
    dest_paths = []
    for comp_id in selected_components:
        comp = registry.find_component(components_dict, comp_id)
        if comp and comp.path:
            dest_path = paths.get_install_path(comp.path, str(cfg.install_dir))
            dest_paths.append(dest_path)

    collision_list = collisions.detect_collisions(dest_paths, str(cfg.install_dir))

    # Determine collision strategy
    collision_strategy = CollisionStrategy.OVERWRITE  # Default for fresh installs
    backup_dir = None

    if collision_list:
        collisions.show_collision_report(collision_list)

        if non_interactive:
            # In non-interactive mode, default to overwrite
            console.print_info("Using default strategy: overwrite")
            collision_strategy = CollisionStrategy.OVERWRITE
        else:
            collision_strategy = collisions.get_collision_strategy()

            if collision_strategy == CollisionStrategy.CANCEL:
                console.print_info("Installation cancelled by user")
                return 0

            # Handle backup
            if collision_strategy == CollisionStrategy.BACKUP:
                console.print_step("Creating backup...")
                backup_dir = collisions.create_backup(
                    collision_list, str(cfg.install_dir)
                )

                if backup_dir:
                    console.print_success(f"Backed up files to {backup_dir}")
                    collision_strategy = CollisionStrategy.OVERWRITE
                else:
                    console.print_error("Backup failed. Installation cancelled.")
                    return 1

    # Perform installation
    result = install_ops.install_components(
        selected_components,
        components_dict,
        str(cfg.install_dir),
        cfg.raw_url,
        cfg.use_local_files,
        cfg.install_dir.parent if cfg.use_local_files else Path.cwd(),
        collision_strategy,
    )

    result.backup_dir = backup_dir

    # Show summary
    report.show_installation_summary(
        result, str(cfg.install_dir), selected_profile, len(selected_components)
    )

    # Show post-install steps
    report.show_post_install(str(cfg.install_dir), cfg.repo_url)

    return 0 if result.failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print_info("\n\nInstallation cancelled by user")
        sys.exit(130)
    except Exception as e:
        console.print_error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
