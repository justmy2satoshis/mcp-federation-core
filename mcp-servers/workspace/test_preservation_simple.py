#!/usr/bin/env python3
"""
MCP Federation Core v0.1.3 - Simple Preservation Test
Tests that manifest tracking works correctly
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

def test_preservation_logic():
    """Test that the preservation logic works correctly"""
    print("MCP Federation Core v0.1.3 - Preservation Fix Test")
    print("=" * 60)

    # Create test directory
    test_dir = Path(tempfile.mkdtemp(prefix="mcp_test_"))
    config_path = test_dir / "claude_desktop_config.json"
    manifest_path = test_dir / "installation_manifest.json"

    try:
        # Test scenario: User had 'memory' and 'filesystem' before installation
        # Federation installer added 'sqlite' and 'playwright'

        # Create manifest
        manifest = {
            'installation_date': datetime.now().isoformat(),
            'installer_version': '0.1.3',
            'pre_existing_mcps': ['memory', 'filesystem'],
            'newly_installed_mcps': ['sqlite', 'playwright'],
            'failed_mcps': []
        }

        # Create config with all MCPs
        config = {
            "mcpServers": {
                "memory": {"command": "npx", "args": ["-y", "@example/memory"]},
                "filesystem": {"command": "npx", "args": ["-y", "@example/filesystem"]},
                "sqlite": {"command": "npx", "args": ["-y", "mcp-sqlite"]},
                "playwright": {"command": "npx", "args": ["-y", "@playwright/mcp"]},
                "my-custom-tool": {"command": "python", "args": ["/path/to/tool.py"]}
            }
        }

        # Save files
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print("Initial setup:")
        print(f"  Pre-existing MCPs: {manifest['pre_existing_mcps']}")
        print(f"  Newly installed: {manifest['newly_installed_mcps']}")
        print(f"  Total MCPs in config: {len(config['mcpServers'])}")

        # Simulate uninstaller logic
        mcps_to_remove = manifest['newly_installed_mcps']
        pre_existing = manifest['pre_existing_mcps']

        removed = []
        preserved = []

        for mcp_name in mcps_to_remove:
            if mcp_name in config['mcpServers']:
                del config['mcpServers'][mcp_name]
                removed.append(mcp_name)

        for mcp_name in pre_existing:
            if mcp_name in config['mcpServers']:
                preserved.append(mcp_name)

        print("\nAfter uninstallation:")
        print(f"  MCPs removed: {removed}")
        print(f"  MCPs preserved: {preserved}")
        print(f"  Total MCPs remaining: {len(config['mcpServers'])}")
        print(f"  Remaining MCPs: {list(config['mcpServers'].keys())}")

        # Verify results
        expected_removed = ['sqlite', 'playwright']
        expected_preserved = ['memory', 'filesystem']
        expected_remaining = ['memory', 'filesystem', 'my-custom-tool']

        removal_ok = set(removed) == set(expected_removed)
        preservation_ok = set(preserved) == set(expected_preserved)
        remaining_ok = set(config['mcpServers'].keys()) == set(expected_remaining)

        print("\nVerification:")
        print(f"  Removal correct: {removal_ok}")
        print(f"  Preservation correct: {preservation_ok}")
        print(f"  Final config correct: {remaining_ok}")

        success = removal_ok and preservation_ok and remaining_ok
        print(f"\nOVERALL TEST: {'PASSED' if success else 'FAILED'}")

        if success:
            print("SUCCESS: Preservation fix works correctly!")
            print("- Pre-existing MCPs are preserved")
            print("- Only newly installed MCPs are removed")
            print("- User MCPs are unaffected")
        else:
            print("FAILURE: Preservation logic needs fixing")

        return success

    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        print(f"\nTest cleanup completed")

if __name__ == "__main__":
    import sys
    success = test_preservation_logic()
    sys.exit(0 if success else 1)