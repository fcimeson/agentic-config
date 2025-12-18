"""Tests for config and environment precedence."""

import os
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from installer_py.config import build_config, detect_repo_slug


class TestConfigPrecedence(unittest.TestCase):
    """Test configuration and environment variable precedence."""

    def setUp(self):
        """Save and clear environment variables."""
        self.saved_env = {}
        env_vars = [
            "OPENCODE_BRANCH",
            "OPENCODE_INSTALL_DIR",
            "OPENCODE_REPO",
            "OPENCODE_RAW_URL",
            "OPENCODE_REGISTRY_URL",
        ]
        for var in env_vars:
            if var in os.environ:
                self.saved_env[var] = os.environ[var]
                del os.environ[var]

    def tearDown(self):
        """Restore environment variables."""
        for var, value in self.saved_env.items():
            os.environ[var] = value

    def test_default_branch(self):
        """Test default branch is 'main'."""
        cfg = build_config()
        self.assertEqual(cfg.branch, "main")

    def test_env_branch_override(self):
        """Test environment variable overrides default branch."""
        os.environ["OPENCODE_BRANCH"] = "develop"
        cfg = build_config()
        self.assertEqual(cfg.branch, "develop")

    def test_arg_branch_override(self):
        """Test argument overrides environment variable."""
        os.environ["OPENCODE_BRANCH"] = "develop"
        cfg = build_config(branch="feature")
        self.assertEqual(cfg.branch, "feature")

    def test_default_install_dir(self):
        """Test default installation directory."""
        cfg = build_config()
        self.assertTrue(str(cfg.install_dir).endswith(".opencode"))

    def test_env_install_dir_override(self):
        """Test environment variable overrides install dir."""
        os.environ["OPENCODE_INSTALL_DIR"] = "/custom/path"
        cfg = build_config()
        self.assertEqual(str(cfg.install_dir), "/custom/path")

    def test_arg_install_dir_override(self):
        """Test argument overrides environment variable for install dir."""
        os.environ["OPENCODE_INSTALL_DIR"] = "/env/path"
        cfg = build_config(install_dir="/arg/path")
        self.assertEqual(str(cfg.install_dir), "/arg/path")

    def test_tilde_expansion(self):
        """Test tilde is expanded in paths."""
        cfg = build_config(install_dir="~/my-agents")
        self.assertNotIn("~", str(cfg.install_dir))
        self.assertTrue(str(cfg.install_dir).endswith("my-agents"))

    def test_default_repo_slug(self):
        """Test default repository slug."""
        cfg = build_config()
        self.assertEqual(cfg.repo_slug, "fcimeson/agentic-config")

    def test_repo_url_construction(self):
        """Test repository URL is constructed correctly."""
        cfg = build_config(repo_slug="user/repo")
        self.assertEqual(cfg.repo_url, "https://github.com/user/repo")

    def test_raw_url_construction(self):
        """Test raw URL is constructed with correct format."""
        cfg = build_config(repo_slug="user/repo", branch="main")
        expected = "https://raw.githubusercontent.com/user/repo/main"
        self.assertEqual(cfg.raw_url, expected)

    def test_explicit_raw_url_override(self):
        """Test explicit raw URL overrides construction."""
        custom_url = "https://custom.example.com/files"
        cfg = build_config(raw_url=custom_url)
        self.assertEqual(cfg.raw_url, custom_url)


if __name__ == "__main__":
    unittest.main()
