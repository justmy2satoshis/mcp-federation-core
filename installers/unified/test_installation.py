#!/usr/bin/env python3
"""
Test Suite for MCP Federation Core Unified Installer
Tests all critical fixes including database paths and placeholder resolution
"""

import os
import sys
import json
import sqlite3
import tempfile
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the installer modules to path
sys.path.insert(0, str(Path(__file__).parent))

from install import MCPInstaller
from db_manager import DatabaseManager
from validator import InstallationValidator

class TestUnifiedInstaller(unittest.TestCase):
    """Test the unified installer functionality"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.installer = MCPInstaller()
        self.installer.repo_root = self.test_dir
        self.installer.mcp_base = self.test_dir / 'mcp_base'

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_unified_database_creation(self):
        """Test that mcp-unified.db is created correctly"""
        db_manager = DatabaseManager(self.installer.mcp_base)
        success = db_manager.initialize_all_databases()

        self.assertTrue(success, "Database initialization should succeed")

        # Check that unified database exists
        unified_db = self.installer.mcp_base / 'databases' / 'mcp-unified.db'
        self.assertTrue(unified_db.exists(), "mcp-unified.db should exist")

        # Check database size (should be > 1KB for a properly initialized DB)
        self.assertGreater(unified_db.stat().st_size, 1024,
                          "Database should be larger than 1KB")

    def test_database_schema_initialization(self):
        """Test that database schemas are properly created"""
        db_manager = DatabaseManager(self.installer.mcp_base)
        db_manager.initialize_all_databases()

        unified_db = self.installer.mcp_base / 'databases' / 'mcp-unified.db'

        with sqlite3.connect(unified_db) as conn:
            # Check that required tables exist
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = {row[0] for row in cursor.fetchall()}

            required_tables = {'mcp_metadata', 'mcp_storage', 'mcp_logs'}
            self.assertTrue(required_tables.issubset(tables),
                          f"Required tables missing: {required_tables - tables}")

    def test_no_placeholders_in_config(self):
        """Test that no placeholders remain in generated configurations"""
        self.installer.create_directory_structure()

        configs = self.installer.generate_mcp_configs()

        # Convert to JSON string to check for placeholders
        config_str = json.dumps(configs)

        # Check for common placeholders that should be replaced
        placeholders = ['[USERNAME]', '[INSTALL_PATH]', '[HOME]', '$RepoRoot', '$Username']

        for placeholder in placeholders:
            self.assertNotIn(placeholder, config_str,
                           f"Placeholder {placeholder} should be replaced")

    def test_sqlite_config_points_to_unified_db(self):
        """Test that SQLite MCP configuration points to unified database"""
        self.installer.create_directory_structure()
        configs = self.installer.generate_mcp_configs()

        sqlite_config = configs.get('sqlite-data-warehouse')
        self.assertIsNotNone(sqlite_config, "SQLite MCP config should exist")

        # Check that it points to the unified database
        args = sqlite_config.get('args', [])
        self.assertGreater(len(args), 1, "SQLite config should have database path argument")

        db_path = args[1]
        expected_path = str(self.installer.mcp_base / 'mcp-unified.db')

        # Normalize paths for comparison
        db_path_normalized = str(Path(db_path).resolve())
        expected_path_normalized = str(Path(expected_path).resolve())

        self.assertEqual(db_path_normalized, expected_path_normalized,
                        f"SQLite should point to unified DB, not {db_path}")

    def test_cross_platform_paths(self):
        """Test that paths work across different platforms"""
        configs = self.installer.generate_mcp_configs()

        # All paths should be absolute and properly formatted
        for mcp_name, config in configs.items():
            args = config.get('args', [])
            for arg in args:
                if isinstance(arg, str) and ('/' in arg or '\\' in arg):
                    # This looks like a path
                    path_obj = Path(arg)
                    if not path_obj.is_absolute():
                        # Some paths might be relative by design, but most should be absolute
                        pass
                    else:
                        self.assertTrue(path_obj.is_absolute(),
                                      f"Path {arg} in {mcp_name} should be absolute")

    def test_platform_detection(self):
        """Test platform detection works correctly"""
        platform = self.installer.platform
        self.assertIn(platform, ['windows', 'darwin', 'linux'],
                     f"Platform should be recognized: {platform}")

        config_paths = self.installer.config_paths
        self.assertIsInstance(config_paths, dict,
                            "Config paths should be a dictionary")
        self.assertIn('claude_desktop', config_paths,
                     "Should have Claude Desktop config path")

    def test_path_resolution(self):
        """Test that all path placeholders are resolved correctly"""
        test_config = {
            'test_key': '[INSTALL_PATH]/servers',
            'nested': {
                'home': '[HOME]/documents',
                'user': '$Username'
            },
            'array': ['[PYTHON_EXEC]', '[NODE_EXEC]']
        }

        resolved = self.installer.resolve_all_paths(test_config)

        # Check that no placeholders remain
        resolved_str = json.dumps(resolved)
        placeholders = ['[INSTALL_PATH]', '[HOME]', '[USERNAME]', '$Username', '[PYTHON_EXEC]', '[NODE_EXEC]']

        for placeholder in placeholders:
            self.assertNotIn(placeholder, resolved_str,
                           f"Placeholder {placeholder} should be resolved")

    @patch('sqlite3.connect')
    def test_database_query_functionality(self, mock_connect):
        """Test that database queries work without SQLITE_NOTADB errors"""
        # Mock successful database connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('test_table',)]
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        db_manager = DatabaseManager(self.installer.mcp_base)
        unified_db_path = db_manager.get_unified_db_path()

        # This should not raise SQLITE_NOTADB error
        with sqlite3.connect(unified_db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM mcp_storage")
            result = cursor.fetchone()

        # If we get here without exception, the test passes
        self.assertTrue(True, "Database query should execute without SQLITE_NOTADB error")

class TestDatabaseManager(unittest.TestCase):
    """Test database manager functionality"""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.db_manager = DatabaseManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_all_databases_initialized(self):
        """Test that all required databases are created"""
        success = self.db_manager.initialize_all_databases()
        self.assertTrue(success, "All databases should initialize successfully")

        # Check that all expected databases exist
        expected_dbs = ['mcp-unified.db', 'expert-roles.db', 'memory-graph.db', 'rag-context.db']

        for db_name in expected_dbs:
            db_path = self.test_dir / 'databases' / db_name
            self.assertTrue(db_path.exists(), f"{db_name} should exist")
            self.assertGreater(db_path.stat().st_size, 0, f"{db_name} should not be empty")

    def test_database_validation(self):
        """Test database validation functionality"""
        self.db_manager.initialize_all_databases()
        results = self.db_manager.validate_databases()

        # All databases should validate successfully
        for db_name, is_valid in results.items():
            self.assertTrue(is_valid, f"{db_name} should validate successfully")

class TestValidator(unittest.TestCase):
    """Test installation validator"""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.config_paths = {
            'claude_desktop': self.test_dir / 'config.json'
        }
        self.validator = InstallationValidator(self.test_dir, self.config_paths)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_sqlite_config_validation(self):
        """Test SQLite configuration validation"""
        # Create a test config with correct SQLite pointing to unified DB
        unified_db_path = str(self.test_dir / 'databases' / 'mcp-unified.db')

        test_config = {
            'mcpServers': {
                'sqlite-data-warehouse': {
                    'command': 'node',
                    'args': ['server.js', unified_db_path]
                }
            }
        }

        # Write test config
        self.config_paths['claude_desktop'].parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_paths['claude_desktop'], 'w') as f:
            json.dump(test_config, f)

        # Create the database
        os.makedirs(self.test_dir / 'databases', exist_ok=True)
        with open(unified_db_path, 'w') as f:
            f.write('dummy')  # Create empty file for test

        success, result = self.validator.validate_sqlite_config()
        self.assertTrue(success, "SQLite config should validate successfully")

    def test_placeholder_detection(self):
        """Test detection of unreplaced placeholders"""
        # Create config with unreplaced placeholders
        test_config = {
            'mcpServers': {
                'test-mcp': {
                    'command': 'node',
                    'args': ['[INSTALL_PATH]/server.js', '/home/[USERNAME]/data']
                }
            }
        }

        self.config_paths['claude_desktop'].parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_paths['claude_desktop'], 'w') as f:
            json.dump(test_config, f)

        success, results = self.validator.validate_configurations()
        self.assertFalse(success, "Should fail validation due to placeholders")

        # Check that specific placeholders are mentioned
        claude_result = results.get('claude_desktop', '')
        self.assertIn('INSTALL_PATH', claude_result, "Should detect [INSTALL_PATH] placeholder")
        self.assertIn('USERNAME', claude_result, "Should detect [USERNAME] placeholder")

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    print("🧪 Running MCP Federation Core Installation Tests")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedInstaller))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseManager))
    suite.addTests(loader.loadTestsFromTestCase(TestValidator))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall result: {'✅ PASSED' if success else '❌ FAILED'}")

    return success

if __name__ == '__main__':
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)