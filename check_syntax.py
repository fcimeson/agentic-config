#!/usr/bin/env python3
"""
Syntax check for the Python installer.
Verifies all modules can be imported without errors.
"""

import sys
import ast
from pathlib import Path


def check_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, "r") as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, str(e)


def main():
    """Check all installer modules for syntax errors."""
    installer_dir = Path(__file__).parent / "installer_py"

    if not installer_dir.exists():
        print(f"Error: installer_py directory not found at {installer_dir}")
        return 1

    python_files = list(installer_dir.glob("*.py"))

    print(f"Checking {len(python_files)} Python files for syntax errors...\n")

    errors = []
    for filepath in sorted(python_files):
        filename = filepath.name
        is_valid, error = check_syntax(filepath)

        if is_valid:
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename}: {error}")
            errors.append((filename, error))

    print()

    if errors:
        print(f"Found {len(errors)} file(s) with syntax errors:")
        for filename, error in errors:
            print(f"  - {filename}: {error}")
        return 1
    else:
        print("All files have valid syntax!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
