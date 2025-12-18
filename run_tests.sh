#!/bin/bash

# Test runner for Python installer
# Run all tests in tests_installer/

echo "Running Python installer tests..."
echo ""

cd "$(dirname "$0")"

# Run each test module
python3 -m unittest tests_installer.test_config
python3 -m unittest tests_installer.test_paths
python3 -m unittest tests_installer.test_registry

echo ""
echo "All tests completed!"
