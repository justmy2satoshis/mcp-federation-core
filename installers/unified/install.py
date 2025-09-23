#!/usr/bin/env python3
"""
MCP Federation Core - Unified Cross-Platform Installer
Fixes critical database path issues and eliminates hardcoded paths
"""

import os
import sys
import json
import sqlite3
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

class MCPInstaller:
    def __init__(self):
        self.platform = platform.system().lower()
        self.home_dir = Path.home()
        self.username = os.getenv('USER') or os.getenv('USERNAME') or 'user'

        # Dynamic path resolution - NO HARDCODING
        self.repo_root = self._find_repo_root()
        self.mcp_base = self.repo_root / 'mcp_base'

        # Platform-specific config paths
        self.config_paths = self._get_config_paths()

        # Executable paths
        self.python_exec = sys.executable
        self.node_exec = shutil.which('node')
        self.npm_exec = shutil.which('npm')

        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)

    def _find_repo_root(self) -> Path:
        """Find repository root by looking for .git directory"""
        current = Path(__file__).parent
        while current != current.parent:
            if (current / '.git').exists():
                return current
            current = current.parent

        # Fallback to script location
        return Path(__file__).parent.parent.parent

    def _get_config_paths(self) -> Dict[str, Path]:
        """Get platform-specific configuration paths"""
        if self.platform == 'windows':
            appdata = Path(os.getenv('APPDATA', self.home_dir / 'AppData' / 'Roaming'))
            return {
                'claude_desktop': appdata / 'Claude' / 'claude_desktop_config.json',
                'claude_code': self.home_dir / '.claude' / 'claude_code_config.json'
            }
        elif self.platform == 'darwin':  # macOS
            return {
                'claude_desktop': self.home_dir / 'Library' / 'Application Support' / 'Claude' / 'claude_desktop_config.json',
                'claude_code': self.home_dir / '.claude' / 'claude_code_config.json'
            }
        else:  # Linux
            config_dir = Path(os.getenv('XDG_CONFIG_HOME', self.home_dir / '.config'))
            return {
                'claude_desktop': config_dir / 'Claude' / 'claude_desktop_config.json',
                'claude_code': self.home_dir / '.claude' / 'claude_code_config.json'
            }

    def detect_claude_installations(self) -> List[str]:
        """Detect which Claude applications are installed"""
        installed = []

        # Check for Claude Desktop
        for config_path in self.config_paths.values():
            if config_path.parent.exists():
                installed.append('claude_desktop')
                break

        # Check for Claude Code CLI
        if shutil.which('claude'):
            installed.append('claude_code')

        return installed

    def check_prerequisites(self) -> Tuple[bool, List[str]]:
        """Check system prerequisites"""
        missing = []

        if not self.python_exec:
            missing.append('Python 3.8+')

        if not self.node_exec:
            missing.append('Node.js 18+')

        if not self.npm_exec:
            missing.append('npm')

        if not shutil.which('git'):
            missing.append('Git')

        return len(missing) == 0, missing

    def create_directory_structure(self):
        """Create required directories"""
        directories = [
            self.mcp_base,
            self.mcp_base / 'databases',
            self.mcp_base / 'servers',
            self.mcp_base / 'logs',
            self.mcp_base / 'backups'
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {directory}")

    def resolve_all_paths(self, config: dict) -> dict:
        """Replace ALL placeholders in configuration with actual paths"""
        if isinstance(config, dict):
            resolved = {}
            for key, value in config.items():
                resolved[key] = self.resolve_all_paths(value)
            return resolved
        elif isinstance(config, list):
            return [self.resolve_all_paths(item) for item in config]
        elif isinstance(config, str):
            # Replace all known placeholders
            replacements = {
                '[INSTALL_PATH]': str(self.mcp_base),
                '[USERNAME]': self.username,
                '[HOME]': str(self.home_dir),
                '[PYTHON_EXEC]': self.python_exec,
                '[NODE_EXEC]': self.node_exec or 'node',
                '[REPO_ROOT]': str(self.repo_root),
                '$RepoRoot': str(self.repo_root),
                '$Username': self.username
            }

            result = config
            for placeholder, replacement in replacements.items():
                result = result.replace(placeholder, replacement)

            # Platform-specific path fixes
            if self.platform == 'windows':
                result = result.replace('/', '\\')
            else:
                result = result.replace('\\', '/')

            return result
        else:
            return config

    def generate_mcp_configs(self) -> Dict[str, dict]:
        """Generate correct MCP configurations with proper database paths"""

        # CRITICAL FIX: SQLite MCP must point to unified database
        unified_db_path = str(self.mcp_base / 'mcp-unified.db')

        configs = {
            'sqlite-data-warehouse': {
                'command': self.node_exec or 'node',
                'args': [
                    str(self.repo_root / 'mcps' / 'sqlite' / 'server.js'),
                    unified_db_path  # FIXED: Points to actual unified database
                ],
                'env': {
                    'NODE_NO_WARNINGS': '1'
                }
            },
            'expert-role-prompt': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'mcps' / 'expert-role-prompt' / 'server.js')]
            },
            'kimi-k2-resilient': {
                'command': self.python_exec,
                'args': [str(self.repo_root / 'mcps' / 'kimi-k2-resilient-enhanced' / 'server.py')]
            },
            'kimi-k2-code-context': {
                'command': self.python_exec,
                'args': [str(self.repo_root / 'mcps' / 'kimi-k2-code-context-enhanced' / 'server.py')]
            },
            'converse-enhanced': {
                'command': self.python_exec,
                'args': [str(self.repo_root / 'mcps' / 'converse-enhanced' / 'server.py')]
            },
            'filesystem': {
                'command': self.node_exec or 'node',
                'args': [
                    str(self.repo_root / 'node_modules' / '@modelcontextprotocol' / 'server-filesystem' / 'dist' / 'index.js'),
                    str(self.home_dir / 'Documents')  # Cross-platform documents folder
                ]
            },
            'memory': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'node_modules' / '@modelcontextprotocol' / 'server-memory' / 'dist' / 'index.js')]
            },
            'sequential-thinking': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'node_modules' / '@modelcontextprotocol' / 'server-sequential-thinking' / 'dist' / 'index.js')]
            },
            'desktop-commander': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'node_modules' / '@wonderwhy-er' / 'desktop-commander' / 'dist' / 'index.js')]
            },
            'playwright': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'node_modules' / '@playwright' / 'mcp' / 'dist' / 'index.js')],
                'env': {'PLAYWRIGHT_BROWSER': 'chromium'}
            },
            'git-ops': {
                'command': self.node_exec or 'node',
                'args': [str(self.repo_root / 'node_modules' / '@cyanheads' / 'git-mcp-server' / 'dist' / 'index.js')],
                'env': {'GIT_REPO_PATH': str(self.repo_root)}
            }
        }

        # Resolve all paths in configs
        return self.resolve_all_paths(configs)

    def install(self) -> bool:
        """Main installation process"""
        self.logger.info("Starting MCP Federation Core installation...")

        # Check prerequisites
        prereq_ok, missing = self.check_prerequisites()
        if not prereq_ok:
            self.logger.error(f"Missing prerequisites: {', '.join(missing)}")
            return False

        # Detect Claude installations
        claude_apps = self.detect_claude_installations()
        if not claude_apps:
            self.logger.warning("No Claude applications detected")

        # Create directory structure
        self.create_directory_structure()

        # Initialize databases (this will be implemented in db_manager.py)
        from .db_manager import DatabaseManager
        db_manager = DatabaseManager(self.mcp_base)
        db_manager.initialize_all_databases()

        # Generate and write configurations
        configs = self.generate_mcp_configs()

        for app in claude_apps:
            config_path = self.config_paths[app]
            self._write_config(config_path, configs)

        self.logger.info("Installation completed successfully!")
        return True

    def _write_config(self, config_path: Path, mcp_configs: Dict[str, dict]):
        """Write MCP configuration to file"""
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config or create new
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        # Ensure mcpServers section exists
        if 'mcpServers' not in config:
            config['mcpServers'] = {}

        # Add our MCP configurations
        config['mcpServers'].update(mcp_configs)

        # Write back to file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        self.logger.info(f"Configuration written to: {config_path}")

if __name__ == '__main__':
    installer = MCPInstaller()
    success = installer.install()
    sys.exit(0 if success else 1)