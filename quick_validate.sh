#!/bin/bash
# Quick validation script to verify Python installer is working

echo "=== Python Installer Quick Validation ==="
echo ""

# Check Python
echo "1. Checking Python version..."
python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }
echo ""

# Check syntax
echo "2. Validating Python syntax..."
python3 check_syntax.py || { echo "ERROR: Syntax errors found"; exit 1; }
echo ""

# Test imports
echo "3. Testing module imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
from installer_py import cli, config, console, platform, paths
from installer_py import registry, network, deps, selection, collisions
from installer_py import install_ops, transform, report, types
print('✓ All imports successful')
" || { echo "ERROR: Import errors"; exit 1; }
echo ""

# Test help
echo "4. Testing --help command..."
python3 install.py --help > /dev/null || { echo "ERROR: Help command failed"; exit 1; }
echo "✓ Help command works"
echo ""

# Test list
echo "5. Testing --list command..."
python3 install.py --list > /dev/null || { echo "ERROR: List command failed"; exit 1; }
echo "✓ List command works"
echo ""

echo "=== All validations passed! ==="
echo ""
echo "The Python installer is ready to use."
echo ""
echo "Try these commands:"
echo "  python3 install.py --help"
echo "  python3 install.py --list"
echo "  python3 install.py developer --install-dir /tmp/test --local-files"
