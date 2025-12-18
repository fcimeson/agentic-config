"""Tests for path handling and transformations."""

import os
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from installer_py.paths import (
    normalize_path,
    validate_install_path,
    get_install_path,
    ensure_parent_dir,
)
from installer_py.transform import transform_context_paths, should_transform


class TestPathHandling(unittest.TestCase):
    """Test path normalization and validation."""

    def test_normalize_absolute_path(self):
        """Test normalizing an absolute path."""
        path = normalize_path("/usr/local/bin")
        self.assertEqual(path, "/usr/local/bin")

    def test_normalize_tilde(self):
        """Test tilde expansion."""
        path = normalize_path("~/my-agents")
        self.assertNotIn("~", path)
        self.assertTrue(path.endswith("my-agents"))

    def test_normalize_backslashes(self):
        """Test backslash conversion (Windows)."""
        path = normalize_path("C:\\Users\\test\\agents")
        self.assertNotIn("\\", path)
        self.assertIn("/", path)

    def test_normalize_trailing_slash(self):
        """Test trailing slashes are removed."""
        path = normalize_path("/usr/local/")
        self.assertFalse(path.endswith("/"))

    def test_get_install_path_strips_opencode(self):
        """Test registry path is converted correctly."""
        registry_path = ".opencode/agent/test.md"
        install_dir = "/custom/install"
        result = get_install_path(registry_path, install_dir)
        expected = "/custom/install/agent/test.md"
        self.assertEqual(result, expected)

    def test_get_install_path_without_opencode_prefix(self):
        """Test path without .opencode prefix."""
        registry_path = "config/test.json"
        install_dir = "/custom/install"
        result = get_install_path(registry_path, install_dir)
        expected = "/custom/install/config/test.json"
        self.assertEqual(result, expected)


class TestPathTransforms(unittest.TestCase):
    """Test path transformation logic."""

    def test_should_transform_local_install(self):
        """Test local installs should not transform."""
        self.assertFalse(should_transform(".opencode"))
        self.assertFalse(should_transform("/path/to/.opencode"))

    def test_should_transform_global_install(self):
        """Test global installs should transform."""
        self.assertTrue(should_transform("~/.config/opencode"))
        self.assertTrue(should_transform("/usr/local/opencode"))

    def test_transform_context_paths_local(self):
        """Test paths are not transformed for local installs."""
        content = "@.opencode/context/test.md and .opencode/context/other.md"
        result = transform_context_paths(content, ".opencode")
        self.assertEqual(result, content)  # Should be unchanged

    def test_transform_context_paths_global(self):
        """Test paths are transformed for global installs."""
        install_dir = "/home/user/.config/opencode"
        content = "@.opencode/context/test.md"
        result = transform_context_paths(content, install_dir)
        expected = f"@{install_dir}/context/test.md"
        self.assertEqual(result, expected)

    def test_transform_both_patterns(self):
        """Test both @ and non-@ patterns are transformed."""
        install_dir = "/home/user/.config/opencode"
        content = "@.opencode/context/a.md and .opencode/context/b.md"
        result = transform_context_paths(content, install_dir)
        self.assertIn(f"@{install_dir}/context/a.md", result)
        self.assertIn(f"{install_dir}/context/b.md", result)


if __name__ == "__main__":
    unittest.main()
