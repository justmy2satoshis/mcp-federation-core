#!/usr/bin/env python3
"""
Post-Installation Validator for MCP Federation Core
Comprehensive validation of installation components
"""

import os
import sys
import json
import sqlite3
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import requests

class InstallationValidator:
    def __init__(self, mcp_base: Path, config_paths: Dict[str, Path]):
        self.mcp_base = mcp_base
        self.config_paths = config_paths
        self.logger = logging.getLogger(__name__)

        self.validation_results = {}

    def validate_prerequisites(self) -> Tuple[bool, Dict[str, str]]:
        """Validate system prerequisites"""
        self.logger.info("🔍 Validating prerequisites...")

        requirements = {
            'Python': {'command': [sys.executable, '--version'], 'min_version': '3.8'},
            'Node.js': {'command': ['node', '--version'], 'min_version': '18.0'},
            'npm': {'command': ['npm', '--version'], 'min_version': '8.0'},
            'Git': {'command': ['git', '--version'], 'min_version': '2.0'}
        }

        results = {}
        all_passed = True

        for name, req in requirements.items():
            try:
                result = subprocess.run(
                    req['command'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if result.returncode == 0:
                    version_output = result.stdout.strip()
                    results[name] = f"✅ {version_output}"
                    self.logger.info(f"  ✅ {name}: {version_output}")
                else:
                    results[name] = f"❌ Command failed"
                    all_passed = False
                    self.logger.error(f"  ❌ {name}: Command failed")

            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                results[name] = f"❌ Not found"
                all_passed = False
                self.logger.error(f"  ❌ {name}: Not found")

        self.validation_results['prerequisites'] = results
        return all_passed, results

    def validate_databases(self) -> Tuple[bool, Dict[str, str]]:
        """Validate database creation and schemas"""
        self.logger.info("🔍 Validating databases...")

        databases_dir = self.mcp_base / 'databases'
        expected_dbs = [
            'mcp-unified.db',
            'expert-roles.db',
            'memory-graph.db',
            'rag-context.db'
        ]

        results = {}
        all_passed = True

        for db_name in expected_dbs:
            db_path = databases_dir / db_name

            if not db_path.exists():
                results[db_name] = "❌ File not found"
                all_passed = False
                self.logger.error(f"  ❌ {db_name}: File not found")
                continue

            # Check file size
            size = db_path.stat().st_size
            if size < 1024:  # Less than 1KB indicates empty or invalid DB
                results[db_name] = f"❌ Invalid size ({size} bytes)"
                all_passed = False
                self.logger.error(f"  ❌ {db_name}: Invalid size ({size} bytes)")
                continue

            # Check database integrity
            try:
                with sqlite3.connect(db_path) as conn:
                    # Check if we can query the database
                    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in cursor.fetchall()]

                    if tables:
                        results[db_name] = f"✅ {len(tables)} tables ({size} bytes)"
                        self.logger.info(f"  ✅ {db_name}: {len(tables)} tables ({size} bytes)")
                    else:
                        results[db_name] = "❌ No tables found"
                        all_passed = False
                        self.logger.error(f"  ❌ {db_name}: No tables found")

            except sqlite3.Error as e:
                results[db_name] = f"❌ SQLite error: {e}"
                all_passed = False
                self.logger.error(f"  ❌ {db_name}: SQLite error: {e}")

        self.validation_results['databases'] = results
        return all_passed, results

    def validate_configurations(self) -> Tuple[bool, Dict[str, str]]:
        """Validate MCP configuration files"""
        self.logger.info("🔍 Validating configurations...")

        results = {}
        all_passed = True

        for app_name, config_path in self.config_paths.items():
            if not config_path.exists():
                results[app_name] = "❌ Config file not found"
                all_passed = False
                self.logger.error(f"  ❌ {app_name}: Config file not found")
                continue

            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)

                # Check for mcpServers section
                if 'mcpServers' not in config:
                    results[app_name] = "❌ No mcpServers section"
                    all_passed = False
                    self.logger.error(f"  ❌ {app_name}: No mcpServers section")
                    continue

                mcp_count = len(config['mcpServers'])

                # Check for placeholders that weren't replaced
                config_str = json.dumps(config)
                placeholders = ['[USERNAME]', '[INSTALL_PATH]', '[HOME]', '$RepoRoot', '$Username']
                found_placeholders = [p for p in placeholders if p in config_str]

                if found_placeholders:
                    results[app_name] = f"❌ Unreplaced placeholders: {', '.join(found_placeholders)}"
                    all_passed = False
                    self.logger.error(f"  ❌ {app_name}: Unreplaced placeholders: {', '.join(found_placeholders)}")
                else:
                    results[app_name] = f"✅ {mcp_count} MCPs configured"
                    self.logger.info(f"  ✅ {app_name}: {mcp_count} MCPs configured")

            except json.JSONDecodeError as e:
                results[app_name] = f"❌ Invalid JSON: {e}"
                all_passed = False
                self.logger.error(f"  ❌ {app_name}: Invalid JSON: {e}")

        self.validation_results['configurations'] = results
        return all_passed, results

    def validate_sqlite_config(self) -> Tuple[bool, str]:
        """Specifically validate SQLite MCP configuration"""
        self.logger.info("🔍 Validating SQLite MCP configuration...")

        for app_name, config_path in self.config_paths.items():
            if not config_path.exists():
                continue

            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)

                sqlite_config = config.get('mcpServers', {}).get('sqlite-data-warehouse')
                if not sqlite_config:
                    continue

                # Check if SQLite points to unified database
                args = sqlite_config.get('args', [])
                if len(args) > 1:
                    db_path = args[1]
                    expected_path = str(self.mcp_base / 'databases' / 'mcp-unified.db')

                    # Normalize paths for comparison
                    db_path_normalized = Path(db_path).resolve()
                    expected_path_normalized = Path(expected_path).resolve()

                    if db_path_normalized == expected_path_normalized:
                        self.logger.info(f"  ✅ SQLite MCP points to unified database")
                        return True, "✅ Points to unified database"
                    else:
                        error_msg = f"❌ Points to wrong database: {db_path}"
                        self.logger.error(f"  {error_msg}")
                        return False, error_msg

            except Exception as e:
                error_msg = f"❌ Error checking SQLite config: {e}"
                self.logger.error(f"  {error_msg}")
                return False, error_msg

        return False, "❌ SQLite MCP configuration not found"

    def validate_unified_database_query(self) -> Tuple[bool, str]:
        """Test actual SQL query on unified database"""
        self.logger.info("🔍 Testing unified database query...")

        unified_db = self.mcp_base / 'databases' / 'mcp-unified.db'

        if not unified_db.exists():
            return False, "❌ Unified database not found"

        try:
            with sqlite3.connect(unified_db) as conn:
                # Test the query that was failing before
                cursor = conn.execute("SELECT COUNT(*) FROM mcp_storage")
                count = cursor.fetchone()[0]

                # Also test table structure
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]

                expected_tables = ['mcp_metadata', 'mcp_storage', 'mcp_logs']
                missing_tables = [t for t in expected_tables if t not in tables]

                if missing_tables:
                    return False, f"❌ Missing tables: {', '.join(missing_tables)}"

                return True, f"✅ Query successful (storage entries: {count})"

        except sqlite3.Error as e:
            return False, f"❌ SQLite error: {e}"

    def validate_api_keys(self) -> Tuple[bool, Dict[str, str]]:
        """Validate API key configuration"""
        self.logger.info("🔍 Validating API keys...")

        env_file = self.mcp_base.parent / '.env'  # .env is in repo root
        results = {}

        if not env_file.exists():
            self.validation_results['api_keys'] = {"status": "❌ No .env file found"}
            return False, {"status": "❌ No .env file found"}

        try:
            with open(env_file, 'r') as f:
                env_content = f.read()

            # Count configured keys
            api_keys = ['MOONSHOT_API_KEY', 'PERPLEXITY_API_KEY', 'OPENAI_API_KEY',
                       'BRAVE_API_KEY', 'XAI_API_KEY', 'ANTHROPIC_API_KEY']

            configured_count = 0
            for key in api_keys:
                if f"{key}=" in env_content and not f"{key}=" in [f"{key}=\n", f"{key}="]:
                    configured_count += 1
                    results[key] = "✅ Configured"
                else:
                    results[key] = "⚠️ Not configured"

            results['summary'] = f"✅ {configured_count}/{len(api_keys)} API keys configured"
            self.logger.info(f"  ✅ {configured_count}/{len(api_keys)} API keys configured")

            self.validation_results['api_keys'] = results
            return configured_count > 0, results

        except Exception as e:
            error_result = {"status": f"❌ Error reading .env: {e}"}
            self.validation_results['api_keys'] = error_result
            return False, error_result

    def validate_cross_mcp_communication(self) -> Tuple[bool, str]:
        """Test cross-MCP communication through unified database"""
        self.logger.info("🔍 Testing cross-MCP communication...")

        unified_db = self.mcp_base / 'databases' / 'mcp-unified.db'

        if not unified_db.exists():
            return False, "❌ Unified database not found"

        try:
            with sqlite3.connect(unified_db) as conn:
                # Insert test data from different MCPs
                test_data = [
                    ('test-mcp-1', 'federation_test', 'Data from MCP 1'),
                    ('test-mcp-2', 'federation_test', 'Data from MCP 2'),
                    ('test-mcp-3', 'federation_test', 'Data from MCP 3')
                ]

                for mcp_name, key, value in test_data:
                    conn.execute(
                        "INSERT OR REPLACE INTO mcp_storage (mcp_name, key, value) VALUES (?, ?, ?)",
                        (mcp_name, key, value)
                    )

                conn.commit()

                # Test cross-MCP query
                cursor = conn.execute(
                    "SELECT mcp_name, value FROM mcp_storage WHERE key = ?",
                    ('federation_test',)
                )

                results = cursor.fetchall()

                if len(results) >= 3:
                    return True, f"✅ Cross-MCP communication working ({len(results)} entries)"
                else:
                    return False, f"❌ Only {len(results)} entries found"

        except sqlite3.Error as e:
            return False, f"❌ Database error: {e}"

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive validation report"""
        self.logger.info("📋 Generating validation report...")

        # Run all validations
        prereq_pass, prereq_results = self.validate_prerequisites()
        db_pass, db_results = self.validate_databases()
        config_pass, config_results = self.validate_configurations()
        sqlite_pass, sqlite_result = self.validate_sqlite_config()
        query_pass, query_result = self.validate_unified_database_query()
        api_pass, api_results = self.validate_api_keys()
        comm_pass, comm_result = self.validate_cross_mcp_communication()

        # Calculate overall score
        total_tests = 7
        passed_tests = sum([prereq_pass, db_pass, config_pass, sqlite_pass, query_pass, api_pass, comm_pass])
        score = (passed_tests / total_tests) * 100

        # Generate report
        report = f"""
{'='*70}
MCP FEDERATION CORE - VALIDATION REPORT
{'='*70}

Overall Score: {score:.1f}% ({passed_tests}/{total_tests} tests passed)

PREREQUISITES:
{self._format_results(prereq_results)}

DATABASES:
{self._format_results(db_results)}

CONFIGURATIONS:
{self._format_results(config_results)}

CRITICAL FIXES:
  SQLite MCP Configuration: {sqlite_result}
  Unified Database Query: {query_result}
  Cross-MCP Communication: {comm_result}

API KEYS:
{self._format_results(api_results)}

{'='*70}
SUMMARY:
{'='*70}

"""

        if score >= 90:
            report += "🎉 EXCELLENT: Installation is ready for production use!\n"
        elif score >= 75:
            report += "✅ GOOD: Installation is functional with minor issues\n"
        elif score >= 50:
            report += "⚠️ PARTIAL: Installation has significant issues that need attention\n"
        else:
            report += "❌ FAILED: Installation has critical issues and is not functional\n"

        report += f"\nDetailed results saved to validation log\n"
        report += f"Database location: {self.mcp_base / 'databases'}\n"
        report += f"Configuration files checked: {len(self.config_paths)}\n"

        return report

    def _format_results(self, results: Dict[str, str]) -> str:
        """Format results dictionary for display"""
        if not results:
            return "  No results\n"

        formatted = ""
        for key, value in results.items():
            formatted += f"  {key}: {value}\n"
        return formatted

    def run_full_validation(self) -> bool:
        """Run full validation suite and return overall success"""
        report = self.generate_comprehensive_report()
        print(report)

        # Save report to file
        report_file = self.mcp_base / 'validation_report.txt'
        with open(report_file, 'w') as f:
            f.write(report)

        self.logger.info(f"Validation report saved to: {report_file}")

        # Return True if critical tests pass
        _, _, _, sqlite_pass, query_pass, _, comm_pass = [
            self.validate_prerequisites(),
            self.validate_databases(),
            self.validate_configurations(),
            self.validate_sqlite_config(),
            self.validate_unified_database_query(),
            self.validate_api_keys(),
            self.validate_cross_mcp_communication()
        ]

        # The most critical issues are SQLite config and database query
        return sqlite_pass[0] and query_pass[0] and comm_pass[0]

if __name__ == '__main__':
    # Test validator
    from pathlib import Path

    mcp_base = Path('test_mcp_base')
    config_paths = {
        'claude_desktop': Path('test_config.json')
    }

    validator = InstallationValidator(mcp_base, config_paths)
    success = validator.run_full_validation()

    print(f"\nValidation {'PASSED' if success else 'FAILED'}")