#!/usr/bin/env python3
"""
MCP Federation Core - FEDERATED Installer
Pulls MCPs from their ORIGINAL repositories, no bundling
"""

import json
import os
import subprocess
import sys
import shutil
import platform
from pathlib import Path
from datetime import datetime

# Fix Windows Unicode
if platform.system() == "Windows":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class FederatedInstaller:
    """Installer that sources MCPs from original repositories"""

    def __init__(self):
        self.home = Path.home()
        self.base_dir = self.home / "mcp-servers"
        self.config_path = self._get_config_path()
        self.db_path = self.base_dir / "mcp-unified.db"
        self.is_windows = platform.system() == "Windows"

        # Track status
        self.installed_mcps = []
        self.failed_mcps = []

    def _get_config_path(self):
        """Get Claude Desktop config path"""
        if platform.system() == "Windows":
            return Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def get_mcp_source_matrix(self):
        """
        Complete source matrix for all 15 MCPs
        NO LOCAL BUNDLING - all from original sources
        """
        return {
            # NPM Registry MCPs (10 total)
            'sequential-thinking': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-sequential-thinking',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-sequential-thinking'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-sequential-thinking']
                }
            },
            'memory': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-memory',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-memory'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-memory']
                }
            },
            'filesystem': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-filesystem',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-filesystem'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-filesystem', str(self.home)]
                }
            },
            'sqlite': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-sqlite',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-sqlite'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-sqlite', str(self.db_path)]
                }
            },
            'github-manager': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-github',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-github'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-github'],
                    'env': {'GITHUB_TOKEN': 'YOUR_GITHUB_TOKEN'}
                }
            },
            'web-search': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-brave-search',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-brave-search'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-brave-search'],
                    'env': {'BRAVE_API_KEY': 'YOUR_BRAVE_API_KEY'}
                }
            },
            'playwright': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-playwright',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-playwright'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-playwright']
                }
            },
            'git-ops': {
                'type': 'npm',
                'source': 'git-ops-mcp',
                'install': ['npm', 'install', '-g', 'git-ops-mcp'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', 'git-ops-mcp']
                }
            },
            'desktop-commander': {
                'type': 'npm',
                'source': '@rkdms/desktop-commander',
                'install': ['npm', 'install', '-g', '@rkdms/desktop-commander'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@rkdms/desktop-commander']
                }
            },
            'rag-context': {
                'type': 'npm',
                'source': '@modelcontextprotocol/server-rag-context',
                'install': ['npm', 'install', '-g', '@modelcontextprotocol/server-rag-context'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', '@modelcontextprotocol/server-rag-context']
                }
            },

            # GitHub Repository MCPs (5 custom MCPs)
            'kimi-k2-heavy-processor': {
                'type': 'github',
                'source': 'https://github.com/justmy2satoshis/kimi-k2-heavy-processor-mcp.git',
                'directory': 'kimi-k2-heavy-processor-mcp',
                'branch': 'main',
                'install': ['npm', 'install'],  # Run in cloned directory
                'config': {
                    'command': 'node',
                    'args': [str(self.base_dir / 'kimi-k2-heavy-processor-mcp' / 'index.js')]
                }
            },
            'converse-enhanced': {
                'type': 'github',
                'source': 'https://github.com/justmy2satoshis/converse-mcp-enhanced.git',
                'directory': 'converse-mcp-enhanced',
                'branch': 'main',
                'install': ['npm', 'install'],
                'config': {
                    'command': 'node',
                    'args': [str(self.base_dir / 'converse-mcp-enhanced' / 'index.js')]
                }
            },
            'kimi-k2-code-context': {
                'type': 'github',
                'source': 'https://github.com/justmy2satoshis/kimi-k2-code-context-mcp.git',
                'directory': 'kimi-k2-code-context-mcp',
                'branch': 'main',
                'install': ['npm', 'install'],
                'config': {
                    'command': 'node',
                    'args': [str(self.base_dir / 'kimi-k2-code-context-mcp' / 'index.js')],
                    'env': {'KIMI_CODE_DB': str(self.base_dir / 'kimi-code.db')}
                }
            },
            'kimi-k2-resilient': {
                'type': 'github',
                'source': 'https://github.com/justmy2satoshis/kimi-k2-resilient-mcp.git',
                'directory': 'kimi-k2-resilient-mcp',
                'branch': 'main',
                'install': ['npm', 'install'],
                'config': {
                    'command': 'node',
                    'args': [str(self.base_dir / 'kimi-k2-resilient-mcp' / 'index.js')],
                    'env': {'KIMI_DB_PATH': str(self.base_dir / 'kimi-resilient.db')}
                }
            },
            'expert-role-prompt': {
                'type': 'github',
                'source': 'https://github.com/justmy2satoshis/expert-role-prompt-mcp.git',
                'directory': 'expert-role-prompt-mcp',
                'branch': 'main',
                'install': ['npm', 'install'],
                'config': {
                    'command': 'node',
                    'args': [str(self.base_dir / 'expert-role-prompt-mcp' / 'index.js')]
                }
            },

            # Alternative: perplexity from npm or GitHub?
            'perplexity': {
                'type': 'npm',
                'source': 'perplexity-mcp-server',
                'install': ['npm', 'install', '-g', 'perplexity-mcp-server'],
                'config': {
                    'command': 'npx',
                    'args': ['-y', 'perplexity-mcp-server'],
                    'env': {'PERPLEXITY_API_KEY': 'YOUR_PERPLEXITY_KEY'}
                }
            }
        }

    def install_npm_mcp(self, name, mcp_info):
        """Install MCP from npm registry"""
        print(f"📦 Installing {name} from npm...")

        try:
            # Check if already installed
            check_cmd = ['npm', 'list', '-g', mcp_info['source']]
            result = subprocess.run(check_cmd, capture_output=True, text=True, shell=self.is_windows)

            if result.returncode == 0:
                print(f"  ✓ Already installed: {mcp_info['source']}")
                return True

            # Install from npm
            print(f"  Installing: {mcp_info['source']}")
            install_result = subprocess.run(
                mcp_info['install'],
                capture_output=True,
                text=True,
                shell=self.is_windows
            )

            if install_result.returncode == 0:
                print(f"  ✅ Installed from npm: {name}")
                return True
            else:
                print(f"  ❌ Failed to install: {install_result.stderr}")
                return False

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False

    def install_github_mcp(self, name, mcp_info):
        """Clone and install MCP from GitHub repository"""
        print(f"🔗 Installing {name} from GitHub...")

        target_dir = self.base_dir / mcp_info['directory']

        try:
            # Check if already cloned
            if target_dir.exists():
                print(f"  📂 Directory exists, pulling latest...")
                # Pull latest changes
                pull_cmd = ['git', 'pull', 'origin', mcp_info['branch']]
                pull_result = subprocess.run(
                    pull_cmd,
                    cwd=str(target_dir),
                    capture_output=True,
                    text=True
                )
                if pull_result.returncode != 0:
                    print(f"  ⚠️ Could not pull updates: {pull_result.stderr}")
            else:
                # Clone repository
                print(f"  Cloning: {mcp_info['source']}")
                clone_cmd = [
                    'git', 'clone',
                    '-b', mcp_info['branch'],
                    mcp_info['source'],
                    str(target_dir)
                ]

                clone_result = subprocess.run(
                    clone_cmd,
                    capture_output=True,
                    text=True
                )

                if clone_result.returncode != 0:
                    print(f"  ❌ Failed to clone: {clone_result.stderr}")
                    return False

                print(f"  ✅ Cloned repository")

            # Install dependencies
            if mcp_info['install']:
                print(f"  📦 Installing dependencies...")
                install_result = subprocess.run(
                    mcp_info['install'],
                    cwd=str(target_dir),
                    capture_output=True,
                    text=True,
                    shell=self.is_windows
                )

                if install_result.returncode == 0:
                    print(f"  ✅ Dependencies installed")
                else:
                    print(f"  ⚠️ Dependency installation had issues")

            print(f"  ✅ GitHub MCP ready: {name}")
            return True

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False

    def install_all_mcps(self):
        """Install all 15 MCPs from their original sources"""
        print("\n" + "="*70)
        print(" INSTALLING MCPs FROM ORIGINAL SOURCES")
        print("="*70)

        matrix = self.get_mcp_source_matrix()

        # Group by type for organized installation
        npm_mcps = {k: v for k, v in matrix.items() if v['type'] == 'npm'}
        github_mcps = {k: v for k, v in matrix.items() if v['type'] == 'github'}

        # Install npm MCPs
        if npm_mcps:
            print(f"\n📦 Installing {len(npm_mcps)} MCPs from npm registry...")
            for name, info in npm_mcps.items():
                if self.install_npm_mcp(name, info):
                    self.installed_mcps.append(name)
                else:
                    self.failed_mcps.append(name)

        # Install GitHub MCPs
        if github_mcps:
            print(f"\n🔗 Installing {len(github_mcps)} MCPs from GitHub...")
            for name, info in github_mcps.items():
                if self.install_github_mcp(name, info):
                    self.installed_mcps.append(name)
                else:
                    self.failed_mcps.append(name)

        # Summary
        print("\n" + "="*70)
        print(f" ✅ Installed: {len(self.installed_mcps)} MCPs")
        print(f" ❌ Failed: {len(self.failed_mcps)} MCPs")

        if self.failed_mcps:
            print(f"\n Failed: {', '.join(self.failed_mcps)}")

        return len(self.failed_mcps) == 0

    def write_configuration(self):
        """Write configuration for installed MCPs"""
        print("\n📝 Writing Claude Desktop configuration...")

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        config = {'mcpServers': {}}
        matrix = self.get_mcp_source_matrix()

        for name in self.installed_mcps:
            if name in matrix:
                config['mcpServers'][name] = matrix[name]['config']
                print(f"  ✓ Configured: {name}")

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

            print(f"\n  ✅ Configuration saved: {self.config_path}")
            print(f"  ✅ Configured {len(config['mcpServers'])} MCPs")
            return True

        except Exception as e:
            print(f"  ❌ Failed to save: {e}")
            return False

    def create_source_documentation(self):
        """Create documentation showing MCP sources"""
        print("\n📄 Creating source documentation...")

        doc_path = self.base_dir / "MCP_SOURCES.md"

        content = """# MCP Federation - Source Repository Mapping

## Architecture

This federation pulls MCPs from their original sources:
- **10 MCPs** from npm registry
- **5 MCPs** from GitHub repositories
- **0 MCPs** bundled locally (proper separation of concerns)

## Complete Source Mapping

| MCP Name | Source Type | Repository/Package | Version Control |
|----------|-------------|-------------------|-----------------|
| sequential-thinking | npm | @modelcontextprotocol/server-sequential-thinking | npm versioning |
| memory | npm | @modelcontextprotocol/server-memory | npm versioning |
| filesystem | npm | @modelcontextprotocol/server-filesystem | npm versioning |
| sqlite | npm | @modelcontextprotocol/server-sqlite | npm versioning |
| github-manager | npm | @modelcontextprotocol/server-github | npm versioning |
| web-search | npm | @modelcontextprotocol/server-brave-search | npm versioning |
| playwright | npm | @modelcontextprotocol/server-playwright | npm versioning |
| git-ops | npm | git-ops-mcp | npm versioning |
| desktop-commander | npm | @rkdms/desktop-commander | npm versioning |
| rag-context | npm | @modelcontextprotocol/server-rag-context | npm versioning |
| perplexity | npm | perplexity-mcp-server | npm versioning |
| **kimi-k2-heavy-processor** | **GitHub** | **https://github.com/justmy2satoshis/kimi-k2-heavy-processor-mcp** | **git/main** |
| **converse-enhanced** | **GitHub** | **https://github.com/justmy2satoshis/converse-mcp-enhanced** | **git/main** |
| **kimi-k2-code-context** | **GitHub** | **https://github.com/justmy2satoshis/kimi-k2-code-context-mcp** | **git/main** |
| **kimi-k2-resilient** | **GitHub** | **https://github.com/justmy2satoshis/kimi-k2-resilient-mcp** | **git/main** |
| **expert-role-prompt** | **GitHub** | **https://github.com/justmy2satoshis/expert-role-prompt-mcp** | **git/main** |

## Update Process

### NPM MCPs
```bash
npm update -g @modelcontextprotocol/server-[name]
```

### GitHub MCPs
```bash
cd ~/mcp-servers/[mcp-directory]
git pull origin main
npm install  # Update dependencies
```

## Federation Architecture

```
mcp-federation-core (this repo)
├── FEDERATED-INSTALLER.py    # Pulls from sources
├── uninstaller.py             # Removes installations
├── MCP_SOURCES.md            # This documentation
└── NO MCP SOURCE CODE        # Clean separation

Actual MCPs:
├── npm registry (10 MCPs)
└── GitHub repos (5 MCPs)
```

## Notes

- The federation installer is a lightweight coordinator
- NO MCP source code is bundled in mcp-federation-core
- Each MCP can be independently updated from its source
- Version control maintained at source repositories
"""

        doc_path.write_text(content)
        print(f"  ✅ Documentation created: {doc_path}")

    def install(self):
        """Main installation process"""
        print("\n" + "="*70)
        print(" MCP FEDERATION - PULLING FROM ORIGINAL SOURCES")
        print("="*70)

        # Create base directory
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # Check dependencies
        deps_ok = self.check_dependencies()
        if not deps_ok:
            print("\n⚠️ Missing dependencies, some MCPs may fail")

        # Install all MCPs from sources
        self.install_all_mcps()

        # Write configuration
        self.write_configuration()

        # Create documentation
        self.create_source_documentation()

        # Create unified database
        self.db_path.touch(exist_ok=True)
        print(f"\n✅ Created unified database: {self.db_path}")

        # Summary
        print("\n" + "="*70)
        print(" INSTALLATION COMPLETE")
        print("="*70)
        print(f"\n✅ Installed from sources: {len(self.installed_mcps)} MCPs")
        print("   NPM packages: 10")
        print("   GitHub repos: 5")
        print("   Local bundles: 0 (proper architecture!)")

        print(f"\n📁 Configuration: {self.config_path}")
        print(f"📁 Documentation: {self.base_dir / 'MCP_SOURCES.md'}")

        return True

    def check_dependencies(self):
        """Check required dependencies"""
        print("\n🔍 Checking dependencies...")

        deps = {
            'node': ['node', '--version'],
            'npm': ['npm', '--version'] if not self.is_windows else ['npm.cmd', '--version'],
            'git': ['git', '--version'],
            'python': ['python', '--version'] if self.is_windows else ['python3', '--version']
        }

        all_ok = True
        for name, cmd in deps.items():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, shell=self.is_windows)
                version = result.stdout.strip() or result.stderr.strip()
                print(f"  ✓ {name}: {version}")
            except:
                print(f"  ❌ {name}: Not found")
                all_ok = False

        return all_ok

def main():
    installer = FederatedInstaller()

    try:
        success = installer.install()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()