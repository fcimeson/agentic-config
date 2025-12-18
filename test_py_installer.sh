#!/bin/bash
# Comprehensive test of Python installer functionality

set -e

echo "=========================================="
echo "Python Installer Test Suite"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass_test() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

fail_test() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
}

info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Test 1: Python version check
echo "Test 1: Python version check"
if python3 --version 2>&1 | grep -q "Python 3"; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    pass_test "Python 3 is installed (version $PYTHON_VERSION)"
else
    fail_test "Python 3 not found"
    exit 1
fi
echo ""

# Test 2: Syntax check
echo "Test 2: Syntax validation"
if python3 check_syntax.py; then
    pass_test "All Python files have valid syntax"
else
    fail_test "Syntax errors found"
fi
echo ""

# Test 3: Import test
echo "Test 3: Module imports"
if python3 test_imports.py 2>&1; then
    pass_test "All modules import successfully"
else
    fail_test "Import errors found"
fi
echo ""

# Test 4: Help command
echo "Test 4: --help command"
if python3 install.py --help > /dev/null 2>&1; then
    pass_test "Help command works"
else
    fail_test "Help command failed"
fi
echo ""

# Test 5: List command
echo "Test 5: --list command"
if python3 install.py --list > /tmp/list-output.txt 2>&1; then
    if grep -q "Available Components" /tmp/list-output.txt; then
        pass_test "List command works and shows components"
    else
        fail_test "List command doesn't show expected output"
    fi
else
    fail_test "List command failed"
fi
echo ""

# Test 6: Profile installation (dry-run style with local files)
echo "Test 6: Developer profile installation"
TEST_DIR="/tmp/test-install-$(date +%s)"
info "Installing to: $TEST_DIR"

if python3 install.py developer --install-dir "$TEST_DIR" --local-files 2>&1 | tee /tmp/install-output.txt; then
    pass_test "Installation completed without errors"
    
    # Verify files were created
    if [ -d "$TEST_DIR" ]; then
        FILE_COUNT=$(find "$TEST_DIR" -type f | wc -l)
        info "Created $FILE_COUNT files"
        
        if [ -f "$TEST_DIR/agent/opencoder.md" ]; then
            pass_test "Agent files installed correctly"
        else
            fail_test "Agent files not found"
        fi
        
        if [ -f "$TEST_DIR/agent/openagent.md" ]; then
            pass_test "OpenAgent installed correctly"
        else
            fail_test "OpenAgent not found"
        fi
        
        if [ -f "$TEST_DIR/command/test.md" ]; then
            pass_test "Command files installed correctly"
        else
            fail_test "Command files not found"
        fi
        
        if [ -f "$TEST_DIR/context/core/essential-patterns.md" ]; then
            pass_test "Context files installed correctly"
        else
            fail_test "Context files not found"
        fi
        
        # Cleanup
        rm -rf "$TEST_DIR"
        pass_test "Cleanup successful"
    else
        fail_test "Installation directory not created"
    fi
else
    fail_test "Installation failed"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
    echo ""
    echo "Some tests failed. Please review the output above."
    exit 1
else
    echo -e "Failed: ${GREEN}0${NC}"
    echo ""
    echo "All tests passed! ✓"
    exit 0
fi
