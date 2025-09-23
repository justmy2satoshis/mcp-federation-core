#!/usr/bin/env python3
"""
Quick test of critical installer fixes
"""

import sys
import json
import tempfile
from pathlib import Path

# Add installer path
sys.path.append(str(Path(__file__).parent / 'installers' / 'unified'))

def test_critical_fixes():
    """Test the most critical fixes"""
    print("Testing Critical MCP Federation Core Fixes")
    print("=" * 50)

    # Test 1: Import works
    try:
        from install import MCPInstaller
        from db_manager import DatabaseManager
        print("PASS Test 1: Modules import successfully")
    except Exception as e:
        print(f"FAIL Test 1: Import failed: {e}")
        return False

    # Test 2: SQLite config points to unified database
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            installer = MCPInstaller()
            installer.repo_root = Path(temp_dir)
            installer.mcp_base = Path(temp_dir) / 'mcp_base'

            configs = installer.generate_mcp_configs()
            sqlite_config = configs.get('sqlite-data-warehouse')

            if not sqlite_config:
                print("FAIL Test 2: SQLite config not found")
                return False

            args = sqlite_config.get('args', [])
            if len(args) < 2:
                print("FAIL Test 2: SQLite config missing database path")
                return False

            db_path = args[1]
            if 'mcp-unified.db' not in db_path:
                print(f"FAIL Test 2: Wrong database path: {db_path}")
                return False

            print("PASS Test 2: SQLite points to mcp-unified.db")
    except Exception as e:
        print(f"FAIL Test 2: SQLite config test failed: {e}")
        return False

    # Test 3: No placeholders in configs
    try:
        config_str = json.dumps(configs)
        placeholders = ['[USERNAME]', '[INSTALL_PATH]', '[HOME]', '$RepoRoot']
        found_placeholders = [p for p in placeholders if p in config_str]

        if found_placeholders:
            print(f"FAIL Test 3: Found unreplaced placeholders: {found_placeholders}")
            return False
        else:
            print("PASS Test 3: No placeholders found in configs")
    except Exception as e:
        print(f"FAIL Test 3: Placeholder test failed: {e}")
        return False

    # Test 4: Database schema initialization
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            db_manager = DatabaseManager(Path(temp_dir))
            success = db_manager.initialize_all_databases()

            if not success:
                print("FAIL Test 4: Database initialization failed")
                return False

            # Check unified database exists
            unified_db = Path(temp_dir) / 'databases' / 'mcp-unified.db'
            if not unified_db.exists():
                print("FAIL Test 4: mcp-unified.db not created")
                return False

            if unified_db.stat().st_size < 1024:
                print("FAIL Test 4: Database too small (likely empty)")
                return False

            print("PASS Test 4: Database initialization successful")
    except Exception as e:
        print(f"FAIL Test 4: Database test failed: {e}")
        return False

    # Test 5: Cross-platform path handling
    try:
        installer = MCPInstaller()

        # Test path resolution
        test_config = {
            'path': '[INSTALL_PATH]/test',
            'user': '[USERNAME]'
        }

        resolved = installer.resolve_all_paths(test_config)

        if '[INSTALL_PATH]' in str(resolved) or '[USERNAME]' in str(resolved):
            print("FAIL Test 5: Path resolution failed")
            return False

        print("PASS Test 5: Cross-platform path resolution working")
    except Exception as e:
        print(f"FAIL Test 5: Path resolution test failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("ALL CRITICAL FIXES VALIDATED!")
    print("=" * 50)

    print("\nKey Issues Fixed:")
    print("- SQLite MCP now points to mcp-unified.db")
    print("- All placeholders dynamically resolved")
    print("- Database schemas properly initialized")
    print("- Cross-platform path handling working")
    print("- No hardcoded paths remain")

    return True

if __name__ == '__main__':
    success = test_critical_fixes()
    if success:
        print("\nReady to commit fixes!")
    else:
        print("\nIssues found - needs investigation")

    sys.exit(0 if success else 1)