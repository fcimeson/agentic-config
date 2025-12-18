#!/usr/bin/env bash

#############################################################################
# OpenCode Component Installer (Wrapper)
# 
# This script is a thin wrapper that locates python3 and executes install.py
# Preserves curl|bash compatibility while using Python for the installer logic
#
# Compatible with:
# - macOS (Python 3.9+)
# - Linux (Python 3.9+)
# - Windows (Git Bash with Python, WSL)
#############################################################################

set -e

# Colors for output
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
CYAN=$'\033[0;36m'
NC=$'\033[0m' # No Color

print_error() {
    printf "%b\n" "${RED}✗${NC} $1"
}

print_info() {
    printf "%b\n" "${BLUE}ℹ${NC} $1"
}

print_success() {
    printf "%b\n" "${GREEN}✓${NC} $1"
}

# Find python3 executable
find_python() {
    # Try common names
    for cmd in python3 python python3.12 python3.11 python3.10 python3.9; do
        if command -v "$cmd" &> /dev/null; then
            # Check if version is 3.9+
            local version=$("$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
            local major=$(echo "$version" | cut -d'.' -f1)
            local minor=$(echo "$version" | cut -d'.' -f2)
            
            if [ "$major" -eq 3 ] && [ "$minor" -ge 9 ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    
    return 1
}

# Main
main() {
    # Find Python
    PYTHON=$(find_python)
    
    if [ -z "$PYTHON" ]; then
        print_error "Python 3.9+ not found"
        echo ""
        echo "Please install Python 3.9 or higher:"
        echo ""
        echo "  macOS:   brew install python3"
        echo "  Ubuntu:  sudo apt-get install python3"
        echo "  Fedora:  sudo dnf install python3"
        echo "  Windows: Download from https://www.python.org/"
        echo ""
        echo "Or use the legacy bash installer:"
        echo "  curl -fsSL https://raw.githubusercontent.com/fcimeson/agentic-config/main/install.sh.bak -o install-bash.sh"
        echo "  bash install-bash.sh"
        exit 1
    fi
    
    local version=$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
    print_info "Using Python $version"
    
    # Check if we're running from a pipe (curl | bash)
    if [ ! -t 0 ]; then
        # Running from pipe - download install.py to temp location
        TEMP_DIR=$(mktemp -d)
        trap 'rm -rf "$TEMP_DIR"' EXIT INT TERM
        
        # Determine repo slug for downloading
        REPO_SLUG="${OPENCODE_REPO:-fcimeson/agentic-config}"
        BRANCH="${OPENCODE_BRANCH:-main}"
        
        print_info "Downloading Python installer..."
        
        if ! command -v curl &> /dev/null; then
            print_error "curl not found (required for remote installation)"
            exit 1
        fi
        
        # Download install.py
        if ! curl -fsSL "https://raw.githubusercontent.com/${REPO_SLUG}/${BRANCH}/install.py" -o "$TEMP_DIR/install.py"; then
            print_error "Failed to download install.py"
            exit 1
        fi
        
        # Download installer_py package
        mkdir -p "$TEMP_DIR/installer_py"
        
        local modules=(
            "__init__.py" "types.py" "console.py" "platform.py" "paths.py"
            "config.py" "cli.py" "registry.py" "network.py" "deps.py"
            "selection.py" "collisions.py" "install_ops.py" "transform.py" "report.py"
        )
        
        for module in "${modules[@]}"; do
            if ! curl -fsSL "https://raw.githubusercontent.com/${REPO_SLUG}/${BRANCH}/installer_py/${module}" \
                -o "$TEMP_DIR/installer_py/${module}"; then
                print_error "Failed to download installer_py/${module}"
                exit 1
            fi
        done
        
        print_success "Installer downloaded"
        
        # Run the installer
        cd "$TEMP_DIR"
        exec "$PYTHON" install.py "$@"
    else
        # Running locally - check if install.py exists
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        if [ ! -f "$SCRIPT_DIR/install.py" ]; then
            print_error "install.py not found in $SCRIPT_DIR"
            echo ""
            echo "Please clone the repository or download both install.sh and install.py"
            exit 1
        fi
        
        # Run the local installer
        exec "$PYTHON" "$SCRIPT_DIR/install.py" "$@"
    fi
}

main "$@"
