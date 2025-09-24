#!/usr/bin/env python3
"""
MCP Federation Core - Clean Uninstaller
Removes federation MCPs while preserving user's original configuration
"""

import json
import os
import shutil
from pathlib import Path
import platform
from datetime import datetime

class MCPUninstaller:
    def __init__(self):
        self.home = Path.home()
        self.base_dir = self.home / "mcp-servers"
        self.config_path = self._get_config_path()
        self.backup_dir = self.base_dir / "backups"

        # List of federation MCPs to remove
        self.federation_mcps = [
            'sequential-thinking', 'memory', 'filesystem', 'sqlite',
            'github-manager', 'web-search', 'playwright', 'git-ops',
            'desktop-commander', 'perplexity', 'expert-role-prompt',
            'converse', 'rag-context', 'kimi-k2-code-context', 'kimi-k2-resilient'
        ]

    def _get_config_path(self):
        """Get the correct Claude Desktop config path for the OS"""
        if platform.system() == "Windows":
            return Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":  # macOS
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def find_latest_backup(self):
        """Find the most recent backup file"""
        if not self.backup_dir.exists():
            return None

        backups = []
        for backup_folder in self.backup_dir.iterdir():
            if backup_folder.is_dir():
                backup_file = backup_folder / "claude_desktop_config.json"
                if backup_file.exists():
                    backups.append(backup_file)

        if backups:
            # Sort by modification time
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return backups[0]

        return None

    def remove_federation_mcps(self):
        """Remove federation MCPs from current configuration"""
        print("\n🗑️  Removing Federation MCPs...")

        if not self.config_path.exists():
            print("  ⚠️  No configuration file found")
            return False

        try:
            # Load current config
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            if 'mcpServers' not in config:
                print("  ⚠️  No MCPs configured")
                return False

            # Count MCPs before removal
            before_count = len(config['mcpServers'])
            removed = []

            # Remove federation MCPs
            for mcp_name in self.federation_mcps:
                if mcp_name in config['mcpServers']:
                    del config['mcpServers'][mcp_name]
                    removed.append(mcp_name)
                    print(f"  ✓ Removed: {mcp_name}")

            # Count MCPs after removal
            after_count = len(config['mcpServers'])

            if removed:
                # Save updated config
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)

                print(f"\n  📊 Summary:")
                print(f"     MCPs before: {before_count}")
                print(f"     MCPs removed: {len(removed)}")
                print(f"     MCPs remaining: {after_count}")

                # List remaining MCPs
                if after_count > 0:
                    print(f"\n  💾 Preserved user MCPs:")
                    for mcp in config['mcpServers'].keys():
                        print(f"     ✓ {mcp}")
            else:
                print("  ℹ️  No federation MCPs found to remove")

            return True

        except Exception as e:
            print(f"  ❌ Error removing MCPs: {e}")
            return False

    def restore_from_backup(self):
        """Restore original configuration from backup"""
        print("\n🔄 Restoring from backup...")

        backup = self.find_latest_backup()
        if not backup:
            print("  ⚠️  No backup found - keeping current config minus federation MCPs")
            return False

        try:
            # Create safety backup of current state
            safety_backup = self.config_path.parent / f"claude_desktop_config.uninstall_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            shutil.copy2(self.config_path, safety_backup)
            print(f"  📦 Safety backup: {safety_backup}")

            # Restore from backup
            shutil.copy2(backup, self.config_path)
            print(f"  ✓ Restored from: {backup}")

            # Verify restoration
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            mcp_count = len(config.get('mcpServers', {}))
            print(f"  ✓ Verified: {mcp_count} MCPs in restored configuration")

            return True

        except Exception as e:
            print(f"  ❌ Error restoring backup: {e}")
            return False

    def clean_federation_files(self):
        """Remove federation-specific files and directories"""
        print("\n🧹 Cleaning federation files...")

        items_to_clean = [
            self.base_dir / "mcp-unified.db",
            self.base_dir / "kimi-code.db",
            self.base_dir / "kimi-resilient.db",
            self.base_dir / "expert-role-prompt",
            self.base_dir / "converse",
            self.base_dir / "rag-context",
            self.base_dir / "kimi-k2-code-context-enhanced",
            self.base_dir / "kimi-k2-resilient-enhanced"
        ]

        for item in items_to_clean:
            if item.exists():
                if item.is_file():
                    item.unlink()
                    print(f"  ✓ Removed file: {item.name}")
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"  ✓ Removed directory: {item.name}")

        print("  ✅ Federation files cleaned")

    def uninstall(self, mode='selective'):
        """Main uninstallation process"""
        print("\n" + "="*70)
        print(" MCP FEDERATION CORE - CLEAN UNINSTALLER")
        print(" Preserving Your Original Configuration")
        print("="*70)

        if mode == 'restore':
            # Try to restore from backup first
            restored = self.restore_from_backup()
            if not restored:
                # Fall back to selective removal
                print("\n  Falling back to selective removal...")
                self.remove_federation_mcps()
        else:
            # Selective removal (default)
            self.remove_federation_mcps()

        # Clean federation files
        clean_files = input("\n❓ Remove federation data files? (y/n): ").lower() == 'y'
        if clean_files:
            self.clean_federation_files()

        print("\n" + "="*70)
        print(" ✅ UNINSTALLATION COMPLETE")
        print("="*70)
        print("\n📋 Next Steps:")
        print("  1. Restart Claude Desktop")
        print("  2. Your original MCPs (if any) are preserved")
        print("  3. Federation MCPs have been removed")

        return True

def main():
    import sys

    uninstaller = MCPUninstaller()

    # Check for mode argument
    mode = 'selective'  # default
    if len(sys.argv) > 1:
        if sys.argv[1] == 'restore':
            mode = 'restore'
        elif sys.argv[1] == 'full':
            mode = 'full'

    try:
        success = uninstaller.uninstall(mode)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Uninstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Uninstallation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()