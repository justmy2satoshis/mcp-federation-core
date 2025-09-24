#!/usr/bin/env python3
"""
Test script for MCP Federation Uninstaller v0.1.0
Validates all uninstaller scenarios
"""

import json
import os
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Import the uninstaller
import sys
sys.path.append(str(Path(__file__).parent))
from uninstaller import FederationUninstaller

class TestFederationUninstaller(unittest.TestCase):
    """Test suite for the federation uninstaller"""

    def setUp(self):
        """Setup test environment"""
        # Create temporary directory for testing
        self.test_dir = Path(tempfile.mkdtemp())
        self.config_dir = self.test_dir / "Claude"
        self.config_dir.mkdir(parents=True)
        self.config_path = self.config_dir / "claude_desktop_config.json"

        # Create test uninstaller with mocked paths
        self.uninstaller = FederationUninstaller()
        self.uninstaller.config_path = self.config_path
        self.uninstaller.base_dir = self.test_dir / ".mcp-federation"
        self.uninstaller.backup_path = self.uninstaller.base_dir / "backup" / "claude_desktop_config.backup.json"

    def tearDown(self):
        """Clean up test environment"""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def create_config(self, mcps):
        """Helper to create a test configuration"""
        config = {
            "mcpServers": {name: {"command": "test"} for name in mcps}
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)

    def test_scenario_1_clean_uninstall(self):
        """Test: Clean uninstall with only federation MCPs"""
        print("\n✅ Test 1: Clean uninstall")

        # Setup: Config with only federation MCPs
        federation_mcps = ['filesystem', 'memory', 'sqlite', 'git-ops', 'playwright']
        self.create_config(federation_mcps)

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertTrue(has_federation)

        # Update configuration
        success = self.uninstaller.update_configuration()
        self.assertTrue(success)

        # Verify all MCPs removed
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        self.assertEqual(len(config['mcpServers']), 0)
        print("  ✓ All federation MCPs removed")
        print("  ✓ Configuration is clean")

    def test_scenario_2_preserve_user_mcps(self):
        """Test: Preserve existing user MCPs"""
        print("\n✅ Test 2: Preserve user MCPs")

        # Setup: Config with mixed MCPs
        all_mcps = [
            'filesystem',  # Federation
            'my-custom-mcp',  # User
            'memory',  # Federation
            'another-user-mcp',  # User
            'sqlite'  # Federation
        ]
        self.create_config(all_mcps)

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertTrue(has_federation)

        # Update configuration
        success = self.uninstaller.update_configuration()
        self.assertTrue(success)

        # Verify only user MCPs remain
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        remaining = list(config['mcpServers'].keys())
        self.assertEqual(len(remaining), 2)
        self.assertIn('my-custom-mcp', remaining)
        self.assertIn('another-user-mcp', remaining)
        self.assertNotIn('filesystem', remaining)
        self.assertNotIn('memory', remaining)
        self.assertNotIn('sqlite', remaining)

        print(f"  ✓ Preserved {len(remaining)} user MCPs")
        print(f"  ✓ Removed federation MCPs")

    def test_scenario_3_no_federation_mcps(self):
        """Test: Handle when no federation MCPs are installed"""
        print("\n✅ Test 3: No federation MCPs")

        # Setup: Config with only user MCPs
        user_mcps = ['custom-tool', 'my-server', 'private-mcp']
        self.create_config(user_mcps)

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertFalse(has_federation)

        # Update configuration (should not change anything)
        success = self.uninstaller.update_configuration()
        self.assertTrue(success)

        # Verify nothing was removed
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        self.assertEqual(len(config['mcpServers']), 3)
        print("  ✓ No federation MCPs found")
        print("  ✓ User MCPs untouched")

    def test_scenario_4_backup_restoration(self):
        """Test: Restore from backup"""
        print("\n✅ Test 4: Backup restoration")

        # Create original config
        original_mcps = ['user-mcp-1', 'user-mcp-2']
        self.create_config(original_mcps)

        # Create backup
        self.uninstaller.backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.config_path, self.uninstaller.backup_path)

        # Modify config to include federation MCPs
        mixed_mcps = original_mcps + ['filesystem', 'memory', 'sqlite']
        self.create_config(mixed_mcps)

        # Restore from backup
        restored = self.uninstaller.restore_backup_if_exists()
        self.assertTrue(restored)

        # Verify original config restored
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        self.assertEqual(len(config['mcpServers']), 2)
        self.assertIn('user-mcp-1', config['mcpServers'])
        self.assertIn('user-mcp-2', config['mcpServers'])

        print("  ✓ Backup found and restored")
        print("  ✓ Original configuration recovered")

    def test_scenario_5_missing_config(self):
        """Test: Handle missing configuration file"""
        print("\n✅ Test 5: Missing configuration")

        # Remove config file
        if self.config_path.exists():
            self.config_path.unlink()

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertFalse(has_federation)

        print("  ✓ Handled missing config gracefully")

    def test_scenario_6_partial_federation(self):
        """Test: Handle partial federation installation"""
        print("\n✅ Test 6: Partial federation")

        # Setup: Only some federation MCPs installed
        partial_mcps = [
            'filesystem',  # Federation
            'user-tool',  # User
            'memory',  # Federation
            # Missing: sqlite, git-ops, etc.
        ]
        self.create_config(partial_mcps)

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertTrue(has_federation)

        # Update configuration
        success = self.uninstaller.update_configuration()
        self.assertTrue(success)

        # Verify partial removal
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        self.assertEqual(len(config['mcpServers']), 1)
        self.assertIn('user-tool', config['mcpServers'])

        print("  ✓ Removed partial federation MCPs")
        print("  ✓ Preserved user MCPs")

    def test_scenario_7_all_15_mcps(self):
        """Test: Verify all 15 federation MCPs are recognized"""
        print("\n✅ Test 7: All 15 federation MCPs")

        # All 15 federation MCPs
        all_federation = [
            'sequential-thinking', 'memory', 'filesystem', 'sqlite',
            'github-manager', 'web-search', 'playwright', 'git-ops',
            'desktop-commander', 'rag-context', 'perplexity',
            'kimi-k2-heavy-processor', 'converse-enhanced',
            'kimi-k2-code-context', 'expert-role-prompt'
        ]

        # Add a user MCP
        all_mcps = all_federation + ['user-custom-mcp']
        self.create_config(all_mcps)

        # Run check
        has_federation = self.uninstaller.check_installation()
        self.assertTrue(has_federation)

        # Update configuration
        success = self.uninstaller.update_configuration()
        self.assertTrue(success)

        # Verify all federation removed, user preserved
        with open(self.config_path, 'r') as f:
            config = json.load(f)

        self.assertEqual(len(config['mcpServers']), 1)
        self.assertIn('user-custom-mcp', config['mcpServers'])

        # Verify none of the federation MCPs remain
        for mcp in all_federation:
            self.assertNotIn(mcp, config['mcpServers'])

        print(f"  ✓ Removed all 15 federation MCPs")
        print(f"  ✓ Preserved user MCP")

def run_tests():
    """Run all uninstaller tests"""
    print("="*70)
    print(" MCP Federation Uninstaller v0.1.0 - Test Suite")
    print("="*70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFederationUninstaller)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED")
        print(f"   • Tests run: {result.testsRun}")
        print(f"   • Success rate: 100%")
    else:
        print("\n❌ SOME TESTS FAILED")
        print(f"   • Tests run: {result.testsRun}")
        print(f"   • Failures: {len(result.failures)}")
        print(f"   • Errors: {len(result.errors)}")

    return result.wasSuccessful()

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)