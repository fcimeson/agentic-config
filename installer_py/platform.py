"""Platform detection and compatibility utilities."""

import sys
import platform


def get_platform_name() -> str:
    """Get the platform name (Linux, macOS, Windows)."""
    system = platform.system()
    if system == "Darwin":
        return "macOS"
    elif system == "Windows":
        return "Windows"
    else:
        return "Linux"


def get_global_install_path() -> str:
    """Get the platform-appropriate global installation path."""
    import os

    # All platforms use XDG standard now
    return os.path.expanduser("~/.config/opencode")


def check_python_version() -> bool:
    """Check if Python version is 3.9+."""
    return sys.version_info >= (3, 9)


def get_python_version_string() -> str:
    """Get a readable Python version string."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
