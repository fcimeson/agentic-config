#!/usr/bin/env python3
"""Quick test to verify installer imports work."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Test imports
    print("Testing imports...")

    from installer_py import cli

    print("✓ cli imported")

    from installer_py import config

    print("✓ config imported")

    from installer_py import console

    print("✓ console imported")

    from installer_py import platform

    print("✓ platform imported")

    from installer_py import paths

    print("✓ paths imported")

    from installer_py import registry

    print("✓ registry imported")

    from installer_py import network

    print("✓ network imported")

    from installer_py import deps

    print("✓ deps imported")

    from installer_py import selection

    print("✓ selection imported")

    from installer_py import collisions

    print("✓ collisions imported")

    from installer_py import install_ops

    print("✓ install_ops imported")

    from installer_py import transform

    print("✓ transform imported")

    from installer_py import report

    print("✓ report imported")

    from installer_py import types

    print("✓ types imported")

    print("\nAll imports successful!")
    print("\nTesting basic functionality...")

    # Test console functions
    console.print_info("Console test message")
    print("✓ Console functions work")

    # Test platform
    global_path = platform.get_global_install_path()
    print(f"✓ Global install path: {global_path}")

    # Test paths
    normalized = paths.normalize_path("~/.opencode")
    print(f"✓ Path normalization works: {normalized}")

    print("\n=== All tests passed! ===")
    sys.exit(0)

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
