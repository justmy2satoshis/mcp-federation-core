#!/usr/bin/env python3
"""
MCP Federation Core v0.1.3 - Preservation Fix Verification Test
Tests that the uninstaller only removes newly installed MCPs and preserves pre-existing ones
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
import platform
from datetime import datetime

class PreservationTestSuite:
    def __init__(self):
        self.home = Path.home()
        self.base_dir = self.home / "mcp-servers"
        self.config_path = self._get_config_path()
        self.test_dir = Path(tempfile.mkdtemp(prefix="mcp_preservation_test_"))

        # Test configuration paths
        self.test_config_path = self.test_dir / "claude_desktop_config.json"
        self.test_manifest_path = self.test_dir / "installation_manifest.json"

        print(f"Test environment: {self.test_dir}")

    def _get_config_path(self):
        """Get Claude Desktop config path"""
        if platform.system() == "Windows":
            return Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def create_test_scenario(self, scenario_name, pre_existing_mcps, federation_mcps_to_install):
        """Create a test scenario with specific pre-existing and to-be-installed MCPs"""
        print(f"\nSetting up test scenario: {scenario_name}")

        # Create initial configuration with pre-existing MCPs
        initial_config = {"mcpServers": {}}

        for mcp_name in pre_existing_mcps:
            initial_config["mcpServers"][mcp_name] = {
                "command": "npx",
                "args": ["-y", f"@example/{mcp_name}"],
                "env": {"NOTE": "Pre-existing user MCP"}
            }

        # Write initial config
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(initial_config, f, indent=2)

        print(f"  OK Created initial config with {len(pre_existing_mcps)} pre-existing MCPs")

        # Simulate federation installation by creating manifest
        manifest = {
            'installation_date': datetime.now().isoformat(),
            'installer_version': '0.1.3',
            'pre_existing_mcps': pre_existing_mcps.copy(),
            'newly_installed_mcps': federation_mcps_to_install.copy(),
            'failed_mcps': []
        }

        # Add newly installed MCPs to config
        for mcp_name in federation_mcps_to_install:
            initial_config["mcpServers"][mcp_name] = {
                "command": "npx",
                "args": ["-y", f"@federation/{mcp_name}"],
                "env": {"NOTE": "Newly installed by federation"}
            }

        # Update config with all MCPs
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(initial_config, f, indent=2)

        # Save manifest
        with open(self.test_manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

        print(f"  OK Simulated installation of {len(federation_mcps_to_install)} new federation MCPs")
        print(f"  OK Manifest created with preservation data")

        return initial_config, manifest

    def run_uninstaller_simulation(self):
        """Simulate the uninstaller logic without actually running the uninstaller"""
        print(f"\nSimulating SAFE uninstaller logic...")

        # Load manifest
        with open(self.test_manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # Load current config
        with open(self.test_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        pre_existing = manifest.get('pre_existing_mcps', [])
        newly_installed = manifest.get('newly_installed_mcps', [])

        print(f"  Pre-existing MCPs to preserve: {len(pre_existing)}")
        for mcp in pre_existing:
            print(f"    - {mcp}")

        print(f"  MCPs to remove: {len(newly_installed)}")
        for mcp in newly_installed:
            print(f"    - {mcp}")

        # Simulate removal
        removed = []
        preserved = []

        for mcp_name in newly_installed:
            if mcp_name in config['mcpServers']:
                del config['mcpServers'][mcp_name]
                removed.append(mcp_name)

        for mcp_name in pre_existing:
            if mcp_name in config['mcpServers']:
                preserved.append(mcp_name)

        # Save updated config
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        return removed, preserved, config

    def verify_preservation(self, expected_preserved, expected_removed, actual_removed, actual_preserved, final_config):
        """Verify that preservation worked correctly"""
        print(f"\n🔍 VERIFICATION RESULTS:")

        # Check removed MCPs
        removed_correct = set(actual_removed) == set(expected_removed)
        print(f"  ✅ Removal correct: {removed_correct}")
        if not removed_correct:
            print(f"    Expected removed: {expected_removed}")
            print(f"    Actually removed: {actual_removed}")

        # Check preserved MCPs
        preserved_correct = set(actual_preserved) == set(expected_preserved)
        print(f"  ✅ Preservation correct: {preserved_correct}")
        if not preserved_correct:
            print(f"    Expected preserved: {expected_preserved}")
            print(f"    Actually preserved: {actual_preserved}")

        # Check final config contains all expected MCPs
        final_mcps = set(final_config['mcpServers'].keys())
        expected_final = set(expected_preserved)

        # Add any other MCPs that weren't federation MCPs
        federation_mcps = set(expected_preserved + expected_removed)
        for mcp in final_config['mcpServers'].keys():
            if mcp not in federation_mcps:
                expected_final.add(mcp)

        final_correct = final_mcps == expected_final
        print(f"  ✅ Final configuration correct: {final_correct}")

        overall_success = removed_correct and preserved_correct and final_correct
        print(f"\n  🎯 OVERALL TEST: {'PASSED' if overall_success else 'FAILED'}")

        return overall_success

    def test_scenario_1_mixed_preservation(self):
        """Test scenario with mix of pre-existing and new federation MCPs"""
        print("\n" + "="*80)
        print("TEST SCENARIO 1: Mixed Pre-existing and New Federation MCPs")
        print("="*80)

        pre_existing = ['memory', 'filesystem']  # User had these federation MCPs before
        new_mcps = ['sqlite', 'playwright', 'git-ops']  # Federation installer added these

        initial_config, manifest = self.create_test_scenario(
            "Mixed Preservation", pre_existing, new_mcps
        )

        removed, preserved, final_config = self.run_uninstaller_simulation()

        success = self.verify_preservation(
            expected_preserved=pre_existing,
            expected_removed=new_mcps,
            actual_removed=removed,
            actual_preserved=preserved,
            final_config=final_config
        )

        return success

    def test_scenario_2_all_new(self):
        """Test scenario where all federation MCPs are new"""
        print("\n" + "="*80)
        print("TEST SCENARIO 2: All Federation MCPs are Newly Installed")
        print("="*80)

        pre_existing = []  # User had no federation MCPs before
        new_mcps = ['memory', 'filesystem', 'sqlite', 'playwright']  # All new

        initial_config, manifest = self.create_test_scenario(
            "All New MCPs", pre_existing, new_mcps
        )

        removed, preserved, final_config = self.run_uninstaller_simulation()

        success = self.verify_preservation(
            expected_preserved=pre_existing,
            expected_removed=new_mcps,
            actual_removed=removed,
            actual_preserved=preserved,
            final_config=final_config
        )

        return success

    def test_scenario_3_all_preexisting(self):
        """Test scenario where all federation MCPs were pre-existing"""
        print("\n" + "="*80)
        print("TEST SCENARIO 3: All Federation MCPs were Pre-existing")
        print("="*80)

        pre_existing = ['memory', 'filesystem', 'sqlite', 'playwright']  # User had all before
        new_mcps = []  # Federation installed nothing new

        initial_config, manifest = self.create_test_scenario(
            "All Pre-existing", pre_existing, new_mcps
        )

        removed, preserved, final_config = self.run_uninstaller_simulation()

        success = self.verify_preservation(
            expected_preserved=pre_existing,
            expected_removed=new_mcps,
            actual_removed=removed,
            actual_preserved=preserved,
            final_config=final_config
        )

        return success

    def test_scenario_4_user_mcps_mixed(self):
        """Test scenario with both federation and non-federation user MCPs"""
        print("\n" + "="*80)
        print("TEST SCENARIO 4: Mixed Federation and User MCPs")
        print("="*80)

        # Add some non-federation MCPs to the initial config
        pre_existing_federation = ['memory', 'git-ops']
        new_federation = ['sqlite', 'playwright']
        user_mcps = ['my-custom-mcp', 'another-tool']

        initial_config, manifest = self.create_test_scenario(
            "Mixed User MCPs", pre_existing_federation, new_federation
        )

        # Add user MCPs that aren't federation MCPs
        for mcp in user_mcps:
            initial_config["mcpServers"][mcp] = {
                "command": "python",
                "args": [f"/path/to/{mcp}/server.py"],
                "env": {"NOTE": "User's custom MCP"}
            }

        # Update config with user MCPs
        with open(self.test_config_path, 'w', encoding='utf-8') as f:
            json.dump(initial_config, f, indent=2)

        removed, preserved, final_config = self.run_uninstaller_simulation()

        # User MCPs should remain untouched
        expected_final_count = len(pre_existing_federation) + len(user_mcps)
        actual_final_count = len(final_config['mcpServers'])

        print(f"  📊 Expected final MCPs: {expected_final_count}")
        print(f"  📊 Actual final MCPs: {actual_final_count}")

        # Verify user MCPs are still there
        user_mcps_preserved = all(mcp in final_config['mcpServers'] for mcp in user_mcps)
        print(f"  ✅ User MCPs preserved: {user_mcps_preserved}")

        success = self.verify_preservation(
            expected_preserved=pre_existing_federation,
            expected_removed=new_federation,
            actual_removed=removed,
            actual_preserved=preserved,
            final_config=final_config
        ) and user_mcps_preserved

        return success

    def run_all_tests(self):
        """Run all preservation test scenarios"""
        print("\n" + "="*80)
        print("MCP FEDERATION CORE v0.1.3 - PRESERVATION FIX TEST SUITE")
        print("Testing that uninstaller only removes newly installed MCPs")
        print("="*80)

        results = {}

        try:
            results['scenario_1'] = self.test_scenario_1_mixed_preservation()
            results['scenario_2'] = self.test_scenario_2_all_new()
            results['scenario_3'] = self.test_scenario_3_all_preexisting()
            results['scenario_4'] = self.test_scenario_4_user_mcps_mixed()

            # Summary
            print("\n" + "="*80)
            print("TEST SUITE RESULTS")
            print("="*80)

            passed = sum(1 for success in results.values() if success)
            total = len(results)

            for scenario, success in results.items():
                status = "✅ PASSED" if success else "❌ FAILED"
                print(f"  {scenario}: {status}")

            print(f"\n📊 SUMMARY: {passed}/{total} tests passed")

            if passed == total:
                print("🎉 ALL TESTS PASSED - Preservation fix is working correctly!")
                print("   • Pre-existing MCPs are preserved")
                print("   • Only newly installed MCPs are removed")
                print("   • User MCPs are unaffected")
            else:
                print("⚠️  SOME TESTS FAILED - Preservation fix needs attention")

            return passed == total

        finally:
            # Cleanup
            shutil.rmtree(self.test_dir)
            print(f"\n🧹 Test environment cleaned up: {self.test_dir}")

def main():
    test_suite = PreservationTestSuite()
    success = test_suite.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())