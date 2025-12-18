#!/bin/bash
# Simple test script for the Python installer

set -e

echo "=== Testing Python Installer ==="
echo ""

# Test 1: Check Python version
echo "Test 1: Checking Python version..."
python3 --version
echo "✓ Python 3 is available"
echo ""

# Test 2: Test --help
echo "Test 2: Testing --help..."
python3 install.py --help
echo "✓ --help works"
echo ""

# Test 3: Test --list
echo "Test 3: Testing --list..."
python3 install.py --list
echo "✓ --list works"
echo ""

# Test 4: Test profile install with local files (non-interactive)
echo "Test 4: Testing developer profile install to /tmp/test-install..."
rm -rf /tmp/test-install
python3 install.py developer --install-dir /tmp/test-install --local-files
echo "✓ Profile installation works"
echo ""

# Test 5: Verify files were installed
echo "Test 5: Verifying installed files..."
if [ -d "/tmp/test-install" ]; then
    echo "✓ Install directory created"
    
    file_count=$(find /tmp/test-install -type f | wc -l)
    echo "  Found $file_count files"
    
    if [ -f "/tmp/test-install/agent/opencoder.md" ]; then
        echo "✓ Agent file installed correctly"
    else
        echo "✗ Agent file not found!"
        exit 1
    fi
else
    echo "✗ Install directory not created!"
    exit 1
fi
echo ""

echo "=== All tests passed! ==="
