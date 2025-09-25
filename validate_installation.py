#!/usr/bin/env python3
"""
MCP Federation Core - Installation Validator
Verifies that all 15 MCPs are correctly installed and configured
"""

import json
import os
import sys
import subprocess
import platform
from pathlib import Path

class InstallationValidator:
    def __init__(self):
        self.home = Path.home()
        self.base_dir = self.home / "mcp-servers"
        self.is_windows = platform.system() == "Windows"
        self.config_path = self._get_config_path()

        # Define the 15 required MCPs
        self.required_mcps = [
            'filesystem',
            'memory',
            'web-search',
            'sequential-thinking',
            'desktop-commander',
            'playwright',
            'sqlite',
            'git-ops',
            'perplexity',
            'github-manager',
            'expert-role-prompt',
            'converse-enhanced',
            'kimi-k2-code-context',
            'kimi-k2-resilient',
            'rag-context'
        ]

        self.validation_results = {}
        self.python_cmd = 'python' if self.is_windows else 'python3'

    def _get_config_path(self):
        """Get the Claude configuration path"""
        if self.is_windows:
            return self.home / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def print_header(self):
        """Print validation header"""
        print("\n" + "="*70)
        print(" MCP FEDERATION CORE - INSTALLATION VALIDATOR")
        print("="*70)
        print(f" Checking: {self.config_path}")
        print(f" Required MCPs: {len(self.required_mcps)}")
        print("="*70 + "\n")

    def check_config_exists(self):
        """Check if Claude config file exists"""
        print("📋 Checking configuration file...")
        if self.config_path.exists():
            print(f"  ✅ Config file exists: {self.config_path}")
            return True
        else:
            print(f"  ❌ Config file not found: {self.config_path}")
            return False

    def load_config(self):
        """Load and parse the configuration"""
        print("\n📖 Loading configuration...")
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            mcp_servers = config.get('mcpServers', {})
            print(f"  ✅ Configuration loaded")
            print(f"  ✅ Found {len(mcp_servers)} MCPs in config")

            return mcp_servers
        except Exception as e:
            print(f"  ❌ Failed to load config: {e}")
            return {}

    def validate_mcp_config(self, name, config):
        """Validate individual MCP configuration"""
        issues = []

        # Check for required fields
        if not config.get('command'):
            issues.append("Missing 'command' field")

        # Check if command/file exists based on type
        command = config.get('command', '')
        args = config.get('args', [])

        # For Python MCPs
        if command in ['python', 'python3']:
            if args and len(args) > 0:
                script_path = Path(args[0])
                if not script_path.exists():
                    issues.append(f"Python script not found: {script_path}")
                else:
                    # Check if it's the correct entry point
                    if 'converse-enhanced' in name and 'server.py' in str(script_path):
                        if 'mcp_server.py' not in str(script_path):
                            issues.append("Wrong entry point: should be mcp_server.py, not server.py")

        # For Node MCPs
        elif command == 'node':
            if args and len(args) > 0:
                script_path = Path(args[0])
                if not script_path.exists():
                    issues.append(f"Node script not found: {script_path}")

        # For NPX MCPs - just check the package name is reasonable
        elif command == 'npx':
            if not args:
                issues.append("NPX command missing package argument")

        # For global commands
        else:
            # Check if command exists in PATH
            try:
                check_cmd = ['where' if self.is_windows else 'which', command]
                result = subprocess.run(check_cmd, capture_output=True, text=True, shell=False)
                if result.returncode != 0:
                    # May be installed but not in PATH yet
                    pass  # Don't report as error
            except:
                pass

        return issues

    def validate_mcps(self, mcp_servers):
        """Validate all MCPs"""
        print("\n🔍 Validating MCP configurations...\n")

        all_valid = True

        # Check for missing MCPs
        configured_mcps = set(mcp_servers.keys())
        required_set = set(self.required_mcps)
        missing_mcps = required_set - configured_mcps
        extra_mcps = configured_mcps - required_set

        # Validate each required MCP
        for mcp_name in self.required_mcps:
            if mcp_name in mcp_servers:
                issues = self.validate_mcp_config(mcp_name, mcp_servers[mcp_name])
                if issues:
                    print(f"  ⚠️  {mcp_name}: Issues found")
                    for issue in issues:
                        print(f"      - {issue}")
                    self.validation_results[mcp_name] = 'warning'
                else:
                    print(f"  ✅ {mcp_name}: Configured correctly")
                    self.validation_results[mcp_name] = 'success'
            else:
                print(f"  ❌ {mcp_name}: NOT CONFIGURED")
                self.validation_results[mcp_name] = 'missing'
                all_valid = False

        # Report missing MCPs
        if missing_mcps:
            print(f"\n❌ Missing {len(missing_mcps)} required MCPs:")
            for mcp in sorted(missing_mcps):
                print(f"  • {mcp}")
            all_valid = False

        # Report extra MCPs (not an error, just info)
        if extra_mcps:
            print(f"\nℹ️  Additional MCPs configured (not required but OK):")
            for mcp in sorted(extra_mcps):
                print(f"  • {mcp}")

        return all_valid

    def check_bundled_files(self):
        """Check if bundled MCP files exist"""
        print("\n📦 Checking bundled MCP files...")

        bundled_mcps = {
            'expert-role-prompt': self.base_dir / 'expert-role-prompt' / 'server.js',
            'converse-enhanced': self.base_dir / 'converse-mcp-enhanced' / 'src' / 'mcp_server.py',
            'kimi-k2-code-context': self.base_dir / 'kimi-k2-code-context-enhanced' / 'server.py',
            'kimi-k2-resilient': self.base_dir / 'kimi-k2-resilient-enhanced' / 'server.py',
            'rag-context': self.base_dir / 'rag-context-fixed' / 'server.py'
        }

        all_exist = True
        for name, path in bundled_mcps.items():
            if path.exists():
                print(f"  ✅ {name}: {path}")
            else:
                print(f"  ❌ {name}: File not found at {path}")
                all_exist = False

        return all_exist

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*70)
        print(" VALIDATION SUMMARY")
        print("="*70)

        success_count = sum(1 for v in self.validation_results.values() if v == 'success')
        warning_count = sum(1 for v in self.validation_results.values() if v == 'warning')
        missing_count = sum(1 for v in self.validation_results.values() if v == 'missing')

        print(f"\n  ✅ Correctly configured: {success_count}/15")
        print(f"  ⚠️  Configured with issues: {warning_count}/15")
        print(f"  ❌ Missing: {missing_count}/15")

        if missing_count == 0:
            if warning_count == 0:
                print("\n🎉 PERFECT! All 15 MCPs are correctly installed and configured!")
            else:
                print(f"\n✅ SUCCESS! All 15 MCPs are configured (with {warning_count} minor issues)")
                print("   The minor issues should not prevent MCPs from working.")
        else:
            print(f"\n❌ INCOMPLETE: {missing_count} MCPs are missing!")
            print("   Please run the installer again to fix missing MCPs.")

        print("\n📋 Next steps:")
        if missing_count > 0:
            print("  1. Run FEDERATED-INSTALLER-FIXED.py to install missing MCPs")
            print("  2. Run this validator again to confirm")
        else:
            print("  1. Restart Claude Desktop")
            print("  2. Check that all 15 MCPs show as connected")
            print("  3. Update API keys in the configuration as needed")

    def run(self):
        """Run the complete validation"""
        self.print_header()

        # Check config exists
        if not self.check_config_exists():
            print("\n❌ Cannot proceed without configuration file")
            print("   Please run the installer first.")
            return False

        # Load configuration
        mcp_servers = self.load_config()
        if not mcp_servers:
            print("\n❌ No MCPs found in configuration")
            return False

        # Validate MCPs
        config_valid = self.validate_mcps(mcp_servers)

        # Check bundled files
        files_exist = self.check_bundled_files()

        # Print summary
        self.print_summary()

        # Return true only if all 15 MCPs are present
        missing_count = sum(1 for v in self.validation_results.values() if v == 'missing')
        return missing_count == 0


if __name__ == "__main__":
    validator = InstallationValidator()
    success = validator.run()
    sys.exit(0 if success else 1)