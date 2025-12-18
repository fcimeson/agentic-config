"""Tests for registry parsing and component lookup."""

import json
import sys
from pathlib import Path
import unittest
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from installer_py.registry import (
    load_registry,
    parse_components,
    parse_profiles,
    find_component,
    get_registry_key,
)
from installer_py.types import ComponentType


# Minimal test registry
TEST_REGISTRY = {
    "version": "1.0.0",
    "components": {
        "agents": [
            {
                "id": "test-agent",
                "name": "Test Agent",
                "path": ".opencode/agent/test-agent.md",
                "description": "A test agent",
                "dependencies": ["subagent:helper"],
            }
        ],
        "subagents": [
            {
                "id": "helper",
                "name": "Helper",
                "path": ".opencode/agent/subagents/helper.md",
                "description": "Helper subagent",
                "dependencies": [],
            }
        ],
        "commands": [],
        "tools": [],
        "plugins": [],
        "contexts": [],
        "config": [
            {
                "id": "env-example",
                "name": "Environment Example",
                "path": "env.example",
                "description": "Example environment file",
                "dependencies": [],
            }
        ],
    },
    "profiles": {
        "test": {
            "name": "Test Profile",
            "description": "For testing",
            "components": ["agent:test-agent", "config:env-example"],
        }
    },
}


class TestRegistryParsing(unittest.TestCase):
    """Test registry loading and parsing."""

    def setUp(self):
        """Create a temporary registry file."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        )
        json.dump(TEST_REGISTRY, self.temp_file)
        self.temp_file.close()
        self.registry_path = Path(self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file."""
        if self.registry_path.exists():
            self.registry_path.unlink()

    def test_load_local_registry(self):
        """Test loading a local registry file."""
        dest_path = Path(tempfile.mktemp(suffix=".json"))

        reg_data = load_registry(
            dest_path, use_local=True, local_path=self.registry_path
        )

        self.assertIsNotNone(reg_data)
        self.assertIsNotNone(reg_data)  # Type guard for mypy
        if reg_data is not None:
            self.assertEqual(reg_data["version"], "1.0.0")

        # Clean up
        if dest_path.exists():
            dest_path.unlink()

    def test_parse_components(self):
        """Test parsing components from registry."""
        components = parse_components(TEST_REGISTRY)

        # Check agents
        self.assertIn(ComponentType.AGENT, components)
        self.assertEqual(len(components[ComponentType.AGENT]), 1)

        agent = components[ComponentType.AGENT][0]
        self.assertEqual(agent.id, "test-agent")
        self.assertEqual(agent.name, "Test Agent")
        self.assertEqual(len(agent.dependencies), 1)

    def test_parse_profiles(self):
        """Test parsing profiles from registry."""
        profiles = parse_profiles(TEST_REGISTRY)

        self.assertIn("test", profiles)
        profile = profiles["test"]
        self.assertEqual(profile.name, "Test Profile")
        self.assertEqual(len(profile.components), 2)

    def test_find_component(self):
        """Test finding a component by ID."""
        components = parse_components(TEST_REGISTRY)

        comp = find_component(components, "agent:test-agent")
        self.assertIsNotNone(comp)
        if comp is not None:  # Type guard
            self.assertEqual(comp.id, "test-agent")
            self.assertEqual(comp.type, ComponentType.AGENT)

    def test_find_component_not_found(self):
        """Test finding a non-existent component returns None."""
        components = parse_components(TEST_REGISTRY)

        comp = find_component(components, "agent:nonexistent")
        self.assertIsNone(comp)

    def test_get_registry_key_plural(self):
        """Test registry key mapping for plural types."""
        self.assertEqual(get_registry_key(ComponentType.AGENT), "agents")
        self.assertEqual(get_registry_key(ComponentType.COMMAND), "commands")

    def test_get_registry_key_singular(self):
        """Test registry key mapping for singular types (config)."""
        self.assertEqual(get_registry_key(ComponentType.CONFIG), "config")


if __name__ == "__main__":
    unittest.main()
