#!/usr/bin/env python3
"""
Safe Uninstaller for MCP Federation Core
Default behavior: SELECTIVE REMOVAL - Only removes Federation components
Preserves user's existing MCPs and configurations
"""

import os
import sys
import json
import shutil
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import argparse

class MCPFederationUninstaller:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platform = self._detect_platform()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define Federation-only MCPs (DO NOT REMOVE USER MCPs BY DEFAULT)
        # COMPLETE list of ALL 15 Federation MCPs with exact names as installed
        self.FEDERATION_MCPS = [
            'sqlite',                        # SQLite data warehouse
            'expert-role-prompt',            # Expert role prompting system
            'kimi-k2-resilient-enhanced',    # Kimi K2 resilient processing
            'kimi-k2-code-context-enhanced', # Kimi K2 code context
            'rag-context',                   # RAG context management
            'converse',                      # Converse provider
            'web-search',                    # Web search capability
            'github-manager',                # GitHub management
            'memory',                        # Memory graph system
            'filesystem',                    # File system access
            'desktop-commander',             # Desktop commander
            'perplexity',                    # Perplexity integration
            'playwright',                    # Playwright browser automation
            'git-ops',                       # Git operations
            'sequential-thinking'            # Sequential thinking
        ]

        # Total expected Federation MCPs
        self.TOTAL_FEDERATION_MCPS = 15

        # Define Federation-specific databases
        self.FEDERATION_DATABASES = [
            'mcp-unified.db',
            'expert-roles.db',
            'memory-graph.db',
            'rag-context.db'
        ]

        # Platform-specific config paths
        self.config_paths = self._get_config_paths()

    def _detect_platform(self) -> str:
        """Detect operating system platform"""
        import platform
        system = platform.system().lower()
        return {
            'windows': 'windows',
            'darwin': 'darwin',
            'linux': 'linux'
        }.get(system, 'linux')

    def _get_config_paths(self) -> Dict[str, Path]:
        """Get platform-specific configuration paths"""
        home = Path.home()

        if self.platform == 'windows':
            return {
                'claude_desktop': home / 'AppData' / 'Roaming' / 'Claude' / 'claude_desktop_config.json',
                'claude_code': home / 'AppData' / 'Roaming' / 'Claude' / 'claude_code_config.json',
                'zed': home / 'AppData' / 'Roaming' / 'Zed' / 'settings.json'
            }
        elif self.platform == 'darwin':
            return {
                'claude_desktop': home / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json',
                'claude_code': home / 'Library' / 'Application Support' / 'Claude' / 'claude_code_config.json',
                'zed': home / '.config' / 'zed' / 'settings.json'
            }
        else:  # Linux
            return {
                'claude_desktop': home / '.config' / 'Claude' / 'claude_desktop_config.json',
                'claude_code': home / '.config' / 'Claude' / 'claude_code_config.json',
                'zed': home / '.config' / 'zed' / 'settings.json'
            }

    def backup_configurations(self) -> Dict[str, Path]:
        """Create backups of all configuration files"""
        print("\n[BACKUP] Creating configuration backups...")
        backups = {}

        backup_dir = Path.cwd() / 'uninstaller_backups' / self.timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)

        for app_name, config_path in self.config_paths.items():
            if config_path.exists():
                backup_path = backup_dir / f"{app_name}_backup.json"
                try:
                    shutil.copy2(config_path, backup_path)
                    backups[app_name] = backup_path
                    print(f"  [OK] Backed up {app_name} configuration")
                except Exception as e:
                    print(f"  [WARN] Could not backup {app_name}: {e}")

        # Save backup manifest
        manifest = {
            'timestamp': self.timestamp,
            'platform': self.platform,
            'backups': {k: str(v) for k, v in backups.items()},
            'original_paths': {k: str(v) for k, v in self.config_paths.items()}
        }

        manifest_path = backup_dir / 'manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"\n[DIR] Backups saved to: {backup_dir}")
        return backups

    def get_installed_mcps(self, config_path: Path) -> Set[str]:
        """Get list of currently installed MCPs from config"""
        if not config_path.exists():
            return set()

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            mcp_servers = config.get('mcpServers', {})
            return set(mcp_servers.keys())
        except Exception as e:
            self.logger.error(f"Error reading config: {e}")
            return set()

    def remove_federation_mcps_only(self, config_path: Path) -> Tuple[int, int]:
        """Remove ONLY Federation MCPs, preserve user MCPs"""
        if not config_path.exists():
            return 0, 0

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            mcp_servers = config.get('mcpServers', {})
            removed_count = 0
            preserved_count = 0

            # Identify MCPs to remove - check exact matches
            mcps_to_remove = []
            for mcp_name in list(mcp_servers.keys()):
                # Check if it's a Federation MCP (exact match)
                if mcp_name in self.FEDERATION_MCPS:
                    mcps_to_remove.append(mcp_name)
                    removed_count += 1
                else:
                    preserved_count += 1

            # Remove Federation MCPs
            for mcp_name in mcps_to_remove:
                del mcp_servers[mcp_name]
                print(f"    [-] Removed: {mcp_name}")

            # Show preserved MCPs
            for mcp_name in mcp_servers.keys():
                print(f"    [+] Preserved: {mcp_name}")

            # Save updated config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)

            return removed_count, preserved_count

        except Exception as e:
            self.logger.error(f"Error updating config: {e}")
            return 0, 0

    def remove_federation_databases(self, mcp_base: Path) -> int:
        """Remove Federation-specific databases only"""
        print("\n[DATABASE] Removing Federation databases...")

        databases_dir = mcp_base / 'databases'
        if not databases_dir.exists():
            print("  [INFO] No databases directory found")
            return 0

        removed_count = 0
        for db_name in self.FEDERATION_DATABASES:
            db_path = databases_dir / db_name
            if db_path.exists():
                try:
                    os.remove(db_path)
                    print(f"  [-] Removed: {db_name}")
                    removed_count += 1
                except Exception as e:
                    print(f"  [WARN] Could not remove {db_name}: {e}")

        # Check for other databases (preserve them)
        remaining_dbs = list(databases_dir.glob('*.db'))
        if remaining_dbs:
            print("\n  Preserved databases:")
            for db in remaining_dbs:
                print(f"    [+] {db.name}")

        return removed_count

    def selective_uninstall(self, mcp_base: Path) -> bool:
        """Perform selective uninstall (DEFAULT MODE)"""
        print("\n" + "="*70)
        print("SELECTIVE UNINSTALL - Removing Federation Components Only")
        print("="*70)
        print("\n[WARNING] This will ONLY remove MCP Federation components")
        print("[OK] Your existing MCPs and configurations will be preserved")

        # Create backups first
        backups = self.backup_configurations()

        # Process each config file
        total_removed = 0
        total_preserved = 0

        for app_name, config_path in self.config_paths.items():
            if config_path.exists():
                print(f"\n[CONFIG] Processing {app_name} configuration...")
                removed, preserved = self.remove_federation_mcps_only(config_path)
                total_removed += removed
                total_preserved += preserved

        # Remove Federation databases
        db_removed = self.remove_federation_databases(mcp_base)

        # Summary
        print("\n" + "="*70)
        print("SELECTIVE UNINSTALL COMPLETE")
        print("="*70)
        print(f"  [-] Federation MCPs removed: {total_removed}")
        print(f"  [+] User MCPs preserved: {total_preserved}")
        print(f"  [DB] Federation databases removed: {db_removed}")
        print(f"  [BACKUP] Backups available at: uninstaller_backups/{self.timestamp}")

        return True

    def complete_uninstall(self, mcp_base: Path) -> bool:
        """Complete uninstall - removes ALL MCPs (use with caution)"""
        print("\n" + "="*70)
        print("[WARNING] COMPLETE UNINSTALL - This will remove ALL MCPs")
        print("="*70)
        print("\n[CRITICAL] WARNING: This will remove:")
        print("  - ALL MCP configurations (Federation AND user MCPs)")
        print("  - ALL databases")
        print("  - ALL MCP-related files")

        confirm = input("\nType 'REMOVE ALL' to confirm complete uninstall: ")
        if confirm != 'REMOVE ALL':
            print("[X] Complete uninstall cancelled")
            return False

        # Create backups
        backups = self.backup_configurations()

        # Remove all MCPs from configs
        for app_name, config_path in self.config_paths.items():
            if config_path.exists():
                print(f"\n[CONFIG] Clearing {app_name} configuration...")
                try:
                    with open(config_path, 'r') as f:
                        config = json.load(f)

                    # Clear all MCPs
                    if 'mcpServers' in config:
                        mcp_count = len(config['mcpServers'])
                        config['mcpServers'] = {}
                        print(f"  [-] Removed {mcp_count} MCPs")

                    with open(config_path, 'w') as f:
                        json.dump(config, f, indent=2)

                except Exception as e:
                    print(f"  [WARN] Error: {e}")

        # Remove entire mcp_base directory
        if mcp_base.exists():
            print(f"\n[DELETE] Removing {mcp_base}...")
            try:
                shutil.rmtree(mcp_base)
                print("  [OK] Directory removed")
            except Exception as e:
                print(f"  ⚠️ Error: {e}")

        print("\n" + "="*70)
        print("COMPLETE UNINSTALL FINISHED")
        print("="*70)
        print(f"[BACKUP] Backups available at: uninstaller_backups/{self.timestamp}")

        return True

    def restore_from_backup(self, backup_dir: Optional[Path] = None) -> bool:
        """Restore configurations from backup"""
        print("\n" + "="*70)
        print("RESTORE FROM BACKUP")
        print("="*70)

        # Find available backups
        backups_root = Path.cwd() / 'uninstaller_backups'
        if not backups_root.exists():
            print("[X] No backups found")
            return False

        # List available backups
        available_backups = sorted(backups_root.glob('*'))
        if not available_backups:
            print("[X] No backups found")
            return False

        if backup_dir is None:
            print("\nAvailable backups:")
            for i, backup in enumerate(available_backups, 1):
                print(f"  {i}. {backup.name}")

            choice = input("\nSelect backup number (or 'q' to quit): ")
            if choice.lower() == 'q':
                return False

            try:
                backup_dir = available_backups[int(choice) - 1]
            except (ValueError, IndexError):
                print("[X] Invalid selection")
                return False

        # Load manifest
        manifest_path = backup_dir / 'manifest.json'
        if not manifest_path.exists():
            print("[X] Invalid backup (no manifest)")
            return False

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Restore each backup
        restored_count = 0
        for app_name, backup_path in manifest['backups'].items():
            backup_file = Path(backup_path)
            original_path = Path(manifest['original_paths'][app_name])

            if backup_file.exists():
                try:
                    shutil.copy2(backup_file, original_path)
                    print(f"  [OK] Restored {app_name}")
                    restored_count += 1
                except Exception as e:
                    print(f"  [WARN] Could not restore {app_name}: {e}")

        print(f"\n[OK] Restored {restored_count} configuration(s)")
        return True

    def analyze_installation(self) -> Dict[str, any]:
        """Enhanced analysis showing all 15 MCPs status"""
        analysis = {
            'federation_mcps_found': [],
            'federation_mcps_missing': [],
            'user_mcps_found': [],
            'total_federation_expected': self.TOTAL_FEDERATION_MCPS,
            'total_federation_found': 0,
            'all_installed_mcps': []
        }

        # Check all config files
        for app_name, config_path in self.config_paths.items():
            if config_path.exists():
                installed_mcps = self.get_installed_mcps(config_path)
                analysis['all_installed_mcps'].extend(installed_mcps)

        # Remove duplicates
        analysis['all_installed_mcps'] = list(set(analysis['all_installed_mcps']))

        # Check each Federation MCP explicitly
        for mcp_name in self.FEDERATION_MCPS:
            if mcp_name in analysis['all_installed_mcps']:
                analysis['federation_mcps_found'].append(mcp_name)
            else:
                analysis['federation_mcps_missing'].append(mcp_name)

        # Find user MCPs (any not in Federation list)
        for mcp in analysis['all_installed_mcps']:
            if mcp not in self.FEDERATION_MCPS:
                analysis['user_mcps_found'].append(mcp)

        analysis['total_federation_found'] = len(analysis['federation_mcps_found'])
        return analysis

    def display_complete_analysis(self, analysis: Dict) -> None:
        """Show status of ALL 15 Federation MCPs"""
        print('\n[ANALYSIS] MCP Federation Status Report:')
        print(f'Expected Federation MCPs: {analysis["total_federation_expected"]}')
        print(f'Currently Installed: {analysis["total_federation_found"]}')
        print(f'Not Installed: {self.TOTAL_FEDERATION_MCPS - analysis["total_federation_found"]}')

        if analysis['federation_mcps_found']:
            print(f'\n[OK] Installed Federation MCPs ({len(analysis["federation_mcps_found"])}):')
            for mcp in sorted(analysis['federation_mcps_found']):
                print(f'  - {mcp}')

        if analysis['federation_mcps_missing']:
            print(f'\n[WARN] Missing Federation MCPs ({len(analysis["federation_mcps_missing"])}):')
            for mcp in sorted(analysis['federation_mcps_missing']):
                print(f'  - {mcp} (not currently installed)')

        if analysis['user_mcps_found']:
            print(f'\n[INFO] User MCPs found ({len(analysis["user_mcps_found"])}):')
            for mcp in sorted(analysis['user_mcps_found']):
                print(f'  + {mcp}')

        print('\n[TARGET] Uninstaller will remove ALL installed Federation MCPs')
        print('         and clean up any Federation directories/databases')

    def dry_run(self, mcp_base: Path) -> None:
        """Perform dry run - show what would be removed"""
        print("\n" + "="*70)
        print("DRY RUN - No changes will be made")
        print("="*70)

        # Use the enhanced analysis
        analysis = self.analyze_installation()
        self.display_complete_analysis(analysis)

        print("\n[LIST] Federation databases that would be removed:")
        databases_dir = mcp_base / 'databases'
        if databases_dir.exists():
            for db_name in self.FEDERATION_DATABASES:
                db_path = databases_dir / db_name
                if db_path.exists():
                    size = db_path.stat().st_size / 1024  # KB
                    print(f"  - {db_name} ({size:.1f} KB)")

        print("\n[OK] Dry run complete - no changes made")

    def interactive_uninstall(self) -> None:
        """Interactive uninstaller with menu"""
        print("\n" + "="*70)
        print("MCP FEDERATION CORE - SAFE UNINSTALLER")
        print("="*70)
        print("\nThis tool safely removes MCP Federation components")
        print("Default mode preserves your existing MCPs")

        # Auto-detect mcp_base
        possible_paths = [
            Path.cwd() / 'mcp_base',
            Path.cwd().parent / 'mcp_base',
            Path.cwd().parent.parent / 'mcp_base',
            Path.home() / 'mcp_base'
        ]

        mcp_base = None
        for path in possible_paths:
            if path.exists():
                mcp_base = path
                break

        if not mcp_base:
            mcp_base_str = input("\nEnter mcp_base path (or press Enter for './mcp_base'): ").strip()
            mcp_base = Path(mcp_base_str) if mcp_base_str else Path.cwd() / 'mcp_base'

        print(f"\nUsing mcp_base: {mcp_base}")

        while True:
            print("\n" + "-"*50)
            print("Select uninstall mode:")
            print("\n  1. SELECTIVE (Recommended) - Remove Federation MCPs only")
            print("  2. COMPLETE - Remove ALL MCPs (use with caution)")
            print("  3. RESTORE - Restore from backup")
            print("  4. DRY RUN - Show what would be removed")
            print("  5. EXIT")

            choice = input("\nChoice (1-5): ").strip()

            if choice == '1':
                self.selective_uninstall(mcp_base)
                break
            elif choice == '2':
                self.complete_uninstall(mcp_base)
                break
            elif choice == '3':
                self.restore_from_backup()
            elif choice == '4':
                self.dry_run(mcp_base)
            elif choice == '5':
                print("\n[EXIT] Uninstaller exited")
                break
            else:
                print("[X] Invalid choice")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Safe uninstaller for MCP Federation Core'
    )

    parser.add_argument(
        '--mode',
        choices=['selective', 'complete', 'restore', 'dry-run'],
        help='Uninstall mode'
    )

    parser.add_argument(
        '--mcp-base',
        type=str,
        help='Path to mcp_base directory'
    )

    parser.add_argument(
        '--backup-dir',
        type=str,
        help='Specific backup directory to restore from'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts (dangerous!)'
    )

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )

    uninstaller = MCPFederationUninstaller()

    if args.mode:
        # Non-interactive mode
        mcp_base = Path(args.mcp_base) if args.mcp_base else Path.cwd() / 'mcp_base'

        if args.mode == 'selective':
            uninstaller.selective_uninstall(mcp_base)
        elif args.mode == 'complete':
            if args.force:
                # Skip confirmation in force mode
                uninstaller.complete_uninstall(mcp_base)
            else:
                uninstaller.complete_uninstall(mcp_base)
        elif args.mode == 'restore':
            backup_dir = Path(args.backup_dir) if args.backup_dir else None
            uninstaller.restore_from_backup(backup_dir)
        elif args.mode == 'dry-run':
            uninstaller.dry_run(mcp_base)
    else:
        # Interactive mode
        uninstaller.interactive_uninstall()

if __name__ == '__main__':
    main()