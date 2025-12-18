"""Tests for the Python installer package."""

import sys
from pathlib import Path

# Add parent directory to path so we can import installer_py
sys.path.insert(0, str(Path(__file__).parent.parent))
