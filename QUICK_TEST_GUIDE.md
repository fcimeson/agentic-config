# Quick Test Guide - Python Installer

## Running Tests

### All Tests
```bash
bash run_tests.sh
```

### Individual Test Modules
```bash
# Config and environment tests
python3 -m unittest tests_installer.test_config

# Path handling tests
python3 -m unittest tests_installer.test_paths

# Registry parsing tests
python3 -m unittest tests_installer.test_registry
```

### Verbose Output
```bash
python3 -m unittest tests_installer.test_config -v
```

## Manual Testing

### Quick Smoke Test
```bash
# Test help
python3 install.py --help

# Test list
python3 install.py --list

# Test with profile (dry run by selecting 'n' when prompted)
python3 install.py essential
```

### Full Interactive Test
```bash
# Run installer interactively
python3 install.py

# Choose:
# 1. Location (local/global/custom)
# 2. Mode (profile/custom)
# 3. Profile
# 4. Confirm or cancel
```

### Non-Interactive Test
```bash
# Install to temp directory
python3 install.py developer --install-dir /tmp/test-opencode

# Verify files
ls -la /tmp/test-opencode/

# Clean up
rm -rf /tmp/test-opencode
```

### Local Files Test
```bash
# Use local registry
python3 install.py --local-files essential

# Verify it uses local files
# Should see "Registry source: local" in output
```

### Collision Test
```bash
# Install once
python3 install.py essential --install-dir /tmp/test-collision

# Install again (should detect collisions)
python3 install.py essential --install-dir /tmp/test-collision

# Try each strategy:
# 1) Skip existing
# 2) Overwrite all
# 3) Backup & overwrite
# 4) Cancel

# Clean up
rm -rf /tmp/test-collision*
```

## Test Commands Summary

```bash
# Unit tests
bash run_tests.sh

# Help and list
python3 install.py --help
python3 install.py --list

# Profiles
python3 install.py essential
python3 install.py developer
python3 install.py business
python3 install.py full
python3 install.py advanced

# Options
python3 install.py developer --install-dir /tmp/test
python3 install.py --local-files
python3 install.py --local-files=/custom/path/registry.json

# Wrapper script
bash install.sh developer
```

## Expected Test Results

### Unit Tests
```
test_config.py: 10 tests ✓
test_paths.py: 11 tests ✓
test_registry.py: 7 tests ✓
Total: 28 tests passing
```

### Manual Tests
- Help displays usage information
- List shows all components grouped by type
- Interactive mode shows menus
- Non-interactive installs without prompts
- Collisions are detected and handled
- Files are installed to correct paths
- Backup creates timestamped directory
- Path transformations work for global installs

## New Validation Scripts (2025-12-18)

### Quick Validation
```bash
bash quick_validate.sh
```
Runs:
1. Python version check
2. Syntax validation
3. Import tests
4. Help command test
5. List command test

### Complete Verification
```bash
bash verify_complete.sh
```
Shows:
- All 15 module files
- All features checklist
- Command examples
- Full implementation status

### Comprehensive Test Suite
```bash
bash test_py_installer.sh
```
Includes:
- Syntax check
- Import verification
- Help command
- List command
- Developer profile installation
- File verification
- Test summary with pass/fail counts

### Syntax Check Only
```bash
python3 check_syntax.py
```
Validates all Python files for syntax errors.

### Import Test Only
```bash
python3 test_imports.py
```
Tests that all modules can be imported successfully.
