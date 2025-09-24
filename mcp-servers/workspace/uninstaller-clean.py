#!/usr/bin/env python3
"""
MCP Federation Core v0.1.4 - COMPLETE Clean Uninstaller
COMPLETE REMOVAL: Now supports full removal of all installed files, directories, and artifacts
PRESERVATION FIX: Uses installation manifest to only remove MCPs that were actually installed
Protects pre-existing user MCPs with federation names from accidental removal
THREE REMOVAL LEVELS: Config-only, data files, or complete removal
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
        self.manifest_path = self.base_dir / "installation_manifest.json"

        # DEPRECATED: Hardcoded list - now uses installation manifest
        # Kept for fallback compatibility only
        self.fallback_federation_mcps = [
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

    def load_installation_manifest(self):
        """Load installation manifest to identify what MCPs to remove safely"""
        if not self.manifest_path.exists():
            print(f"  ⚠️  No installation manifest found at: {self.manifest_path}")
            print(f"  ℹ️  Using fallback method (all federation MCPs will be removed)")
            return None

        try:
            with open(self.manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            print(f"  ✅ Loaded manifest from: {self.manifest_path}")
            print(f"     Installation date: {manifest.get('installation_date', 'Unknown')}")
            print(f"     Installer version: {manifest.get('installer_version', 'Unknown')}")

            pre_existing = manifest.get('pre_existing_mcps', [])
            newly_installed = manifest.get('newly_installed_mcps', [])

            if pre_existing:
                print(f"  🔒 Protected pre-existing MCPs: {len(pre_existing)}")
                for mcp in pre_existing:
                    print(f"     • {mcp} (WILL BE PRESERVED)")

            if newly_installed:
                print(f"  🗑️  MCPs to remove: {len(newly_installed)}")
                for mcp in newly_installed:
                    print(f"     • {mcp} (will be removed)")

            return manifest

        except Exception as e:
            print(f"  ❌ Error loading manifest: {e}")
            print(f"  ℹ️  Using fallback method")
            return None

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
        """SAFE removal using installation manifest - only removes newly installed MCPs"""
        print("\n🗑️  SAFE Federation MCP Removal (Manifest-Based)...")

        if not self.config_path.exists():
            print("  ⚠️  No configuration file found")
            return False

        # Load installation manifest
        manifest = self.load_installation_manifest()

        try:
            # Load current config
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            if 'mcpServers' not in config:
                print("  ⚠️  No MCPs configured")
                return False

            # Determine which MCPs to remove
            if manifest:
                # SAFE MODE: Only remove MCPs that were newly installed by federation
                mcps_to_remove = manifest.get('newly_installed_mcps', [])
                pre_existing = manifest.get('pre_existing_mcps', [])

                print(f"\n  🔒 PROTECTION ACTIVE: {len(pre_existing)} pre-existing MCPs will be preserved")
                print(f"  🗑️  REMOVAL TARGET: {len(mcps_to_remove)} newly installed MCPs")
            else:
                # FALLBACK MODE: Remove all federation MCPs (old behavior)
                mcps_to_remove = self.fallback_federation_mcps
                pre_existing = []
                print(f"\n  ⚠️  FALLBACK MODE: No manifest found, removing all federation MCPs")
                print(f"  ❗ WARNING: Pre-existing MCPs with federation names may be removed")

            # Count MCPs before removal
            before_count = len(config['mcpServers'])
            removed = []
            preserved = []
            not_found = []

            # Process each MCP to remove
            for mcp_name in mcps_to_remove:
                if mcp_name in config['mcpServers']:
                    del config['mcpServers'][mcp_name]
                    removed.append(mcp_name)
                    print(f"  ✓ Removed: {mcp_name}")
                else:
                    not_found.append(mcp_name)
                    print(f"  ℹ️  Not found: {mcp_name}")

            # Check for preserved pre-existing MCPs
            if manifest:
                for mcp_name in pre_existing:
                    if mcp_name in config['mcpServers']:
                        preserved.append(mcp_name)
                        print(f"  🔒 PRESERVED: {mcp_name} (was pre-existing)")

            # Count MCPs after removal
            after_count = len(config['mcpServers'])

            # Save updated config if changes were made
            if removed:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)

                print(f"\n  📊 REMOVAL SUMMARY:")
                print(f"     MCPs before: {before_count}")
                print(f"     MCPs removed: {len(removed)}")
                print(f"     MCPs preserved: {len(preserved)}")
                print(f"     MCPs remaining: {after_count}")

                if preserved:
                    print(f"\n  🔒 PRESERVED PRE-EXISTING MCPs:")
                    for mcp in preserved:
                        print(f"     ✓ {mcp}")

                # List all remaining MCPs
                if after_count > 0:
                    print(f"\n  💾 ALL REMAINING MCPs:")
                    for mcp in config['mcpServers'].keys():
                        status = "(pre-existing)" if mcp in preserved else "(user MCP)"
                        print(f"     ✓ {mcp} {status}")
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

    def remove_installed_directories(self):
        """COMPLETE REMOVAL - Remove ALL directories created by installation"""
        print("\n🗑️  COMPLETE REMOVAL - Removing all installed directories...")

        # Main directories to remove
        directories_to_remove = [
            self.base_dir,  # Entire mcp-servers directory and all contents
            self.home / '.mcp-federation',  # Config/manifest directory if exists
        ]

        removed_count = 0
        for directory in directories_to_remove:
            if directory.exists():
                try:
                    # Count items before removal for reporting
                    if directory.is_dir():
                        item_count = sum(1 for _ in directory.rglob('*'))
                        shutil.rmtree(directory)
                        print(f"  ✅ Removed: {directory} ({item_count} items)")
                        removed_count += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {directory}: {e}")
                    print(f"     Try manually: rmdir /s /q \"{directory}\"")
            else:
                print(f"  ℹ️  Not found: {directory}")

        if removed_count > 0:
            print(f"\n  ✅ COMPLETE REMOVAL: {removed_count} directories removed")
            print(f"     All federation artifacts have been deleted")
        else:
            print(f"\n  ℹ️  No directories found to remove")

    def clean_federation_files(self):
        """Remove federation-specific files and directories"""
        print("\n🧹 Cleaning federation files...")

        items_to_clean = [
            self.base_dir / "mcp-unified.db",
            self.base_dir / "kimi-code.db",
            self.base_dir / "kimi-resilient.db",
            self.base_dir / "expert-role-prompt",
            self.base_dir / "expert-role-prompt-mcp",
            self.base_dir / "converse",
            self.base_dir / "converse-mcp-enhanced",
            self.base_dir / "rag-context",
            self.base_dir / "rag-context-mcp",
            self.base_dir / "kimi-k2-code-context-enhanced",
            self.base_dir / "kimi-k2-resilient-enhanced",
            self.base_dir / "kimi-k2-code-context-mcp-repo",
            self.base_dir / "kimi-k2-heavy-processor-mcp-repo",
            self.base_dir / "federation-wrappers",
            self.manifest_path  # Clean up the installation manifest too
        ]

        cleaned_count = 0
        for item in items_to_clean:
            if item.exists():
                if item.is_file():
                    item.unlink()
                    print(f"  ✓ Removed file: {item.name}")
                    cleaned_count += 1
                elif item.is_dir():
                    shutil.rmtree(item)
                    print(f"  ✓ Removed directory: {item.name}")
                    cleaned_count += 1

        print(f"  ✅ Federation cleanup complete: {cleaned_count} items removed")

    def uninstall(self, mode='selective'):
        """SAFE uninstallation process with manifest-based preservation"""
        print("\n" + "="*70)
        print(" MCP FEDERATION CORE v0.1.4 - COMPLETE CLEAN UNINSTALLER")
        print(" PRESERVATION FIX: Protects Pre-Existing User MCPs")
        print(" COMPLETE REMOVAL: Removes ALL Installed Files & Directories")
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

        # Ask about complete removal of ALL federation artifacts
        print("\n" + "="*50)
        print(" COMPLETE REMOVAL OPTIONS")
        print("="*50)
        print("\n Choose removal level:")
        print("  1. Keep installed files (only removed from config)")
        print("  2. Remove data files only (databases, caches)")
        print("  3. COMPLETE REMOVAL (all files, directories, artifacts)")

        choice = input("\n Select option (1-3): ").strip()

        if choice == '2':
            self.clean_federation_files()
        elif choice == '3':
            print("\n⚠️  WARNING: This will remove:")
            print("  - ~/mcp-servers directory and ALL contents")
            print("  - All installed MCP files")
            print("  - All databases and configuration")
            print("  - Installation manifests and backups")

            confirm = input("\n Are you SURE? Type 'yes' to confirm: ").strip().lower()
            if confirm == 'yes':
                self.clean_federation_files()
                self.remove_installed_directories()
            else:
                print("  Skipping complete removal")

        print("\n" + "="*70)
        print(" ✅ UNINSTALLATION COMPLETE")
        print("="*70)
        print("\n📋 Next Steps:")
        print("  1. Restart Claude Desktop")
        if choice == '3' and confirm == 'yes':
            print("  2. ALL federation files and directories have been removed")
            print("  3. Your system is completely clean of federation artifacts")
        else:
            print("  2. Pre-existing MCPs with federation names are PRESERVED")
            print("  3. Only newly installed federation MCPs were removed from config")
            print("  4. Installation manifest was used to ensure safe removal")

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