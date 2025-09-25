#!/usr/bin/env python3
"""
MCP Federation Core v0.1.0 - Safe Uninstaller
Copyright (c) 2025 justmy2satoshis
Licensed under MIT License

Safely removes the 15 federated MCPs while preserving user's original setup
"""

import json
import os
import subprocess
import shutil
import sys
import platform
from pathlib import Path
from datetime import datetime
import logging

# Fix Windows Unicode
if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class FederationUninstaller:
    """
    Safe uninstaller that:
    - Removes ONLY the 15 federation MCPs
    - Preserves ALL user's original MCPs
    - Handles partial installations
    - Provides rollback capability
    """

    def __init__(self):
        self.home = Path.home()
        self.base_dir = self.home / ".mcp-federation"
        self.config_path = self._get_config_path()
        self.backup_path = self.base_dir / "backup" / "claude_desktop_config.backup.json"
        self.log_file = self.base_dir / f"uninstall_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.is_windows = platform.system() == "Windows"

        # Setup logging
        self._setup_logging()

        # The 15 federation MCPs
        self.FEDERATION_MCPS = {
            # NPM packages (11)
            'sequential-thinking': '@modelcontextprotocol/server-sequential-thinking',
            'memory': '@modelcontextprotocol/server-memory',
            'filesystem': '@modelcontextprotocol/server-filesystem',
            'sqlite': '@modelcontextprotocol/server-sqlite',
            'github-manager': '@modelcontextprotocol/server-github',
            'web-search': '@modelcontextprotocol/server-brave-search',
            'playwright': '@modelcontextprotocol/server-playwright',
            'git-ops': 'git-ops-mcp',
            'desktop-commander': '@rkdms/desktop-commander',
            'rag-context': '@modelcontextprotocol/server-rag-context',
            'perplexity': 'perplexity-mcp-server',

            # GitHub clones (4)
            'kimi-k2-heavy-processor': 'github:justmy2satoshis/kimi-k2-heavy-processor-mcp',
            'converse-enhanced': 'github:justmy2satoshis/converse-mcp-enhanced',
            'kimi-k2-code-context': 'github:justmy2satoshis/kimi-k2-code-context-mcp',
            'expert-role-prompt': 'github:justmy2satoshis/expert-role-prompt-mcp'
        }

        # Track operations
        self.removed_mcps = []
        self.failed_removals = []
        self.preserved_mcps = []

    def _setup_logging(self):
        """Setup logging for uninstall operations"""
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _get_config_path(self):
        """Get Claude Desktop config path for the current OS"""
        if platform.system() == "Windows":
            return Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":  # macOS
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def display_header(self):
        """Display uninstaller header with version"""
        print("="*70)
        print(" MCP Federation Core v0.1.0 - Safe Uninstaller")
        print(" Preserving Your Original Configuration")
        print("="*70)
        print()
        self.logger.info("Starting MCP Federation Uninstaller v0.1.0")

    def check_installation(self):
        """Check what's currently installed"""
        print("🔍 Checking current installation...")

        # Check config
        if not self.config_path.exists():
            print("  ⚠️  No Claude Desktop configuration found")
            self.logger.warning("No configuration file found")
            return False

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            mcp_servers = config.get('mcpServers', {})

            # Categorize MCPs
            federation_found = []
            user_mcps = []

            for mcp_name in mcp_servers.keys():
                if mcp_name in self.FEDERATION_MCPS:
                    federation_found.append(mcp_name)
                else:
                    user_mcps.append(mcp_name)

            # Display findings
            print(f"\n📊 Current Configuration:")
            print(f"  • Total MCPs: {len(mcp_servers)}")
            print(f"  • Federation MCPs: {len(federation_found)}")
            print(f"  • User MCPs: {len(user_mcps)}")

            if federation_found:
                print(f"\n🎯 Federation MCPs to remove:")
                for mcp in federation_found:
                    print(f"  - {mcp}")

            if user_mcps:
                print(f"\n💾 User MCPs to preserve:")
                for mcp in user_mcps:
                    print(f"  ✓ {mcp}")
                    self.preserved_mcps.append(mcp)

            return len(federation_found) > 0

        except Exception as e:
            print(f"  ❌ Error checking installation: {e}")
            self.logger.error(f"Error checking installation: {e}")
            return False

    def confirm_uninstall(self):
        """Get user confirmation before proceeding"""
        print("\n" + "="*70)
        print(" ⚠️  UNINSTALLATION CONFIRMATION")
        print("="*70)
        print("\nThis will:")
        print("  • Remove the 15 federation MCPs")
        print("  • Preserve any non-federation MCPs")
        print("  • Restore your original configuration (if backup exists)")
        print("  • Optionally remove the unified database")

        response = input("\nProceed with uninstallation? (y/N): ").lower().strip()
        return response == 'y'

    def create_safety_backup(self):
        """Create a safety backup before making changes"""
        print("\n💾 Creating safety backup...")

        if not self.config_path.exists():
            print("  ⚠️  No configuration to backup")
            return True

        try:
            safety_dir = self.base_dir / "safety_backups"
            safety_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safety_backup = safety_dir / f"config_before_uninstall_{timestamp}.json"

            shutil.copy2(self.config_path, safety_backup)
            print(f"  ✓ Safety backup created: {safety_backup.name}")
            self.logger.info(f"Safety backup created: {safety_backup}")

            return True

        except Exception as e:
            print(f"  ❌ Failed to create safety backup: {e}")
            self.logger.error(f"Failed to create safety backup: {e}")
            return False

    def remove_npm_packages(self):
        """Remove npm-installed MCPs"""
        print("\n📦 Removing npm packages...")

        npm_mcps = {
            name: pkg for name, pkg in self.FEDERATION_MCPS.items()
            if not pkg.startswith('github:')
        }

        for mcp_name, package_name in npm_mcps.items():
            try:
                print(f"  Removing {mcp_name}...", end=' ')

                # Use npm.cmd on Windows
                npm_cmd = 'npm.cmd' if self.is_windows else 'npm'

                result = subprocess.run(
                    [npm_cmd, 'uninstall', '-g', package_name],
                    capture_output=True,
                    text=True,
                    shell=self.is_windows
                )

                if result.returncode == 0:
                    print("✓")
                    self.removed_mcps.append(mcp_name)
                    self.logger.info(f"Removed npm package: {package_name}")
                else:
                    print("⚠️ (may not be installed)")
                    self.logger.warning(f"Package may not be installed: {package_name}")

            except Exception as e:
                print(f"❌")
                self.failed_removals.append(mcp_name)
                self.logger.error(f"Failed to remove {package_name}: {e}")

    def remove_github_clones(self):
        """Remove GitHub cloned MCPs"""
        print("\n🗂️  Removing GitHub clones...")

        github_dir = self.base_dir / "github-mcps"

        github_mcps = {
            name: pkg.replace('github:', '') for name, pkg in self.FEDERATION_MCPS.items()
            if pkg.startswith('github:')
        }

        for mcp_name, repo_path in github_mcps.items():
            repo_name = repo_path.split('/')[-1]
            clone_path = github_dir / repo_name

            if clone_path.exists():
                try:
                    print(f"  Removing {mcp_name}...", end=' ')
                    shutil.rmtree(clone_path)
                    print("✓")
                    self.removed_mcps.append(mcp_name)
                    self.logger.info(f"Removed GitHub clone: {clone_path}")
                except Exception as e:
                    print("❌")
                    self.failed_removals.append(mcp_name)
                    self.logger.error(f"Failed to remove {clone_path}: {e}")
            else:
                print(f"  {mcp_name} not found (skipping)")

    def remove_wrapper_scripts(self):
        """Remove wrapper scripts created for unified database"""
        print("\n🔧 Removing wrapper scripts...")

        wrapper_dir = self.base_dir / "wrappers"

        if wrapper_dir.exists():
            try:
                shutil.rmtree(wrapper_dir)
                print("  ✓ Wrapper scripts removed")
                self.logger.info("Removed wrapper scripts")
            except Exception as e:
                print(f"  ⚠️  Could not remove wrappers: {e}")
                self.logger.warning(f"Could not remove wrappers: {e}")

    def update_configuration(self):
        """Remove federation MCPs from Claude Desktop config"""
        print("\n📝 Updating configuration...")

        if not self.config_path.exists():
            print("  ⚠️  No configuration to update")
            return True

        try:
            # Load current config
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            mcp_servers = config.get('mcpServers', {})
            initial_count = len(mcp_servers)

            # Remove federation MCPs
            for mcp_name in list(self.FEDERATION_MCPS.keys()):
                if mcp_name in mcp_servers:
                    del mcp_servers[mcp_name]
                    print(f"  ✓ Removed from config: {mcp_name}")

            final_count = len(mcp_servers)
            removed_count = initial_count - final_count

            # Save updated config
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

            print(f"\n  📊 Configuration updated:")
            print(f"     • Removed: {removed_count} MCPs")
            print(f"     • Preserved: {final_count} MCPs")

            self.logger.info(f"Configuration updated: removed {removed_count}, preserved {final_count}")

            return True

        except Exception as e:
            print(f"  ❌ Failed to update configuration: {e}")
            self.logger.error(f"Failed to update configuration: {e}")
            return False

    def restore_backup_if_exists(self):
        """Restore original configuration from backup if available"""
        print("\n🔄 Checking for original backup...")

        if self.backup_path.exists():
            try:
                print(f"  ✓ Found backup from installation")

                # Load backup to verify
                with open(self.backup_path, 'r', encoding='utf-8') as f:
                    backup_config = json.load(f)

                backup_mcp_count = len(backup_config.get('mcpServers', {}))
                print(f"  📊 Backup contains {backup_mcp_count} MCPs")

                # Restore backup
                shutil.copy2(self.backup_path, self.config_path)
                print(f"  ✓ Original configuration restored")

                self.logger.info(f"Restored configuration from {self.backup_path}")

                return True

            except Exception as e:
                print(f"  ⚠️  Could not restore backup: {e}")
                self.logger.warning(f"Could not restore backup: {e}")
                return False
        else:
            print("  ℹ️  No backup found (using updated configuration)")
            return False

    def handle_database(self):
        """Handle unified database cleanup"""
        print("\n💾 Database cleanup...")

        db_path = self.base_dir / "databases" / "mcp-unified.db"

        if db_path.exists():
            print(f"  Found unified database: {db_path}")
            print(f"  Size: {db_path.stat().st_size / 1024:.1f} KB")

            response = input("\n  Remove unified database? (y/N): ").lower().strip()

            if response == 'y':
                try:
                    # Backup database first
                    backup_dir = self.base_dir / "database_backups"
                    backup_dir.mkdir(parents=True, exist_ok=True)

                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    db_backup = backup_dir / f"mcp-unified_{timestamp}.db"

                    shutil.copy2(db_path, db_backup)
                    print(f"  📦 Database backed up to: {db_backup.name}")

                    # Remove database
                    db_path.unlink()
                    print("  ✓ Unified database removed")

                    self.logger.info(f"Database removed (backed up to {db_backup})")

                except Exception as e:
                    print(f"  ❌ Failed to remove database: {e}")
                    self.logger.error(f"Failed to remove database: {e}")
            else:
                print("  ℹ️  Database preserved (can be reused if reinstalling)")
        else:
            print("  ℹ️  No unified database found")

    def cleanup_directories(self):
        """Clean up federation directories if empty"""
        print("\n🧹 Cleaning up directories...")

        # Check if base directory is empty
        if self.base_dir.exists():
            # Keep logs and backups
            keep_dirs = ['safety_backups', 'database_backups', 'backup']

            for item in self.base_dir.iterdir():
                if item.is_dir() and item.name not in keep_dirs:
                    if not any(item.iterdir()):  # If empty
                        try:
                            item.rmdir()
                            print(f"  ✓ Removed empty directory: {item.name}")
                        except:
                            pass

    def display_summary(self):
        """Display uninstallation summary"""
        print("\n" + "="*70)
        print(" 📊 UNINSTALLATION SUMMARY")
        print("="*70)

        print(f"\n✅ Successfully removed: {len(self.removed_mcps)} MCPs")
        if self.removed_mcps:
            for mcp in self.removed_mcps[:5]:  # Show first 5
                print(f"   • {mcp}")
            if len(self.removed_mcps) > 5:
                print(f"   ... and {len(self.removed_mcps) - 5} more")

        if self.failed_removals:
            print(f"\n⚠️  Failed to remove: {len(self.failed_removals)} MCPs")
            for mcp in self.failed_removals:
                print(f"   • {mcp}")

        if self.preserved_mcps:
            print(f"\n💾 Preserved user MCPs: {len(self.preserved_mcps)}")
            for mcp in self.preserved_mcps:
                print(f"   ✓ {mcp}")

        print(f"\n📄 Uninstall log: {self.log_file}")

        print("\n" + "="*70)
        print(" ✅ UNINSTALLATION COMPLETE")
        print("="*70)

        print("\n📋 Next Steps:")
        print("  1. Restart Claude Desktop")
        print("  2. Your original MCPs are preserved")
        print("  3. You can reinstall federation anytime")

    def uninstall(self):
        """Main uninstallation process"""
        try:
            # Display header
            self.display_header()

            # Check what's installed
            has_federation = self.check_installation()

            if not has_federation:
                print("\n✅ No federation MCPs found to remove")
                print("   Your configuration is already clean.")
                return True

            # Get confirmation
            if not self.confirm_uninstall():
                print("\n❌ Uninstallation cancelled")
                self.logger.info("User cancelled uninstallation")
                return False

            # Create safety backup
            if not self.create_safety_backup():
                response = input("\n⚠️  Continue without safety backup? (y/N): ").lower().strip()
                if response != 'y':
                    print("\n❌ Uninstallation cancelled")
                    return False

            # Remove npm packages
            self.remove_npm_packages()

            # Remove GitHub clones
            self.remove_github_clones()

            # Remove wrapper scripts
            self.remove_wrapper_scripts()

            # Try to restore backup first
            if not self.restore_backup_if_exists():
                # Fall back to updating current config
                self.update_configuration()

            # Handle database
            self.handle_database()

            # Clean up directories
            self.cleanup_directories()

            # Display summary
            self.display_summary()

            return True

        except KeyboardInterrupt:
            print("\n\n⚠️  Uninstallation interrupted by user")
            self.logger.warning("Uninstallation interrupted by user")
            return False

        except Exception as e:
            print(f"\n❌ Uninstallation error: {e}")
            self.logger.error(f"Uninstallation error: {e}")

            print("\n📋 Manual Recovery:")
            print("  1. Check safety backup in: ~/.mcp-federation/safety_backups/")
            print("  2. Restore manually if needed")
            print("  3. Contact support with the log file")

            return False

def main():
    """Entry point with argument handling"""
    import argparse

    parser = argparse.ArgumentParser(
        description='MCP Federation Core v0.1.0 - Safe Uninstaller'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be removed without making changes'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts (use with caution)'
    )
    parser.add_argument(
        '--keep-database',
        action='store_true',
        help='Keep the unified database (for reinstallation)'
    )

    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("\nThis would remove the following:")
        print("\n15 Federation MCPs:")
        mcps = [
            'sequential-thinking', 'memory', 'filesystem', 'sqlite',
            'github-manager', 'web-search', 'playwright', 'git-ops',
            'desktop-commander', 'rag-context', 'perplexity',
            'kimi-k2-heavy-processor', 'converse-enhanced',
            'kimi-k2-code-context', 'expert-role-prompt'
        ]
        for mcp in mcps:
            print(f"  - {mcp}")
        print("\nYour original MCPs would be preserved.")
        sys.exit(0)

    # Run uninstaller
    uninstaller = FederationUninstaller()

    if args.force:
        # Override confirmation method
        uninstaller.confirm_uninstall = lambda: True

    if args.keep_database:
        # Override database handling
        uninstaller.handle_database = lambda: print("\n💾 Database preserved (--keep-database flag)")

    success = uninstaller.uninstall()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()