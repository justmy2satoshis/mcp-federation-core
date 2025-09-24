#!/usr/bin/env python3
"""
MCP Federation Core v0.1.2 - DIAGNOSTIC SCRIPT
Identifies exact failure points for all MCP configurations
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import platform

def test_command_exists(command):
    """Test if a command exists in PATH"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['where', command], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', command], capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        return False, str(e)

def test_script_exists(script_path):
    """Test if a script file exists"""
    return Path(script_path).exists()

def test_npm_package_exists(package_name):
    """Test if npm package exists in registry"""
    try:
        result = subprocess.run(['npm', 'view', package_name, 'name'],
                              capture_output=True, text=True, shell=platform.system() == "Windows")
        return result.returncode == 0, result.stdout.strip() if result.returncode == 0 else result.stderr
    except Exception as e:
        return False, str(e)

def test_github_repo_exists(repo_url):
    """Test if GitHub repository exists"""
    try:
        result = subprocess.run(['git', 'ls-remote', '--heads', repo_url],
                              capture_output=True, text=True)
        return result.returncode == 0, "Repository accessible" if result.returncode == 0 else result.stderr
    except Exception as e:
        return False, str(e)

def test_mcp_configuration(name, config):
    """Test if MCP configuration is valid"""
    issues = []

    # Test command
    command = config.get('command')
    if not command:
        return ['No command specified']

    cmd_exists, cmd_info = test_command_exists(command)
    if not cmd_exists:
        issues.append(f'Command not found: {command}')

    # Test args for script paths
    args = config.get('args', [])
    if command in ['python', 'python3', 'node'] and args:
        script_path = args[0] if args else None
        if script_path and not script_path.startswith('-'):  # Skip flags
            if not test_script_exists(script_path):
                issues.append(f'Script not found: {script_path}')

    # Test for specific package issues
    if command == 'npx' and args:
        package = args[1] if len(args) > 1 and args[0] == '-y' else args[0]

        # Check known problematic packages
        problematic_packages = {
            '@modelcontextprotocol/server-sqlite': 'Package does not exist - use "mcp-sqlite" instead',
            '@modelcontextprotocol/server-playwright': 'Package does not exist - use "@playwright/mcp" instead',
            'git-ops-mcp': 'Package does not exist - use "@cyanheads/git-mcp-server" instead',
            '@rkdms/desktop-commander': 'Package does not exist - use "@wonderwhy-er/desktop-commander" instead'
        }

        if package in problematic_packages:
            issues.append(problematic_packages[package])
        else:
            # Test if package exists in npm registry
            pkg_exists, pkg_info = test_npm_package_exists(package)
            if not pkg_exists:
                issues.append(f'NPM package not found: {package} - {pkg_info[:100]}...' if len(pkg_info) > 100 else pkg_info)

    return issues if issues else ['OK']

def main():
    print("=" * 70)
    print(" MCP FEDERATION CORE v0.1.2 - DIAGNOSTIC REPORT")
    print("=" * 70)

    # Load configuration
    home = Path.home()
    if platform.system() == "Windows":
        config_path = Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
    elif platform.system() == "Darwin":
        config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        config_path = home / ".config" / "Claude" / "claude_desktop_config.json"

    if not config_path.exists():
        print(f"❌ Configuration file not found: {config_path}")
        return 1

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return 1

    mcp_servers = config.get('mcpServers', {})
    if not mcp_servers:
        print("❌ No MCP servers found in configuration")
        return 1

    print(f"\nTesting {len(mcp_servers)} MCP configurations...\n")

    # Test each MCP
    total_mcps = len(mcp_servers)
    working_mcps = 0
    failed_mcps = 0

    for name, mcp_config in mcp_servers.items():
        print(f"Testing: {name}")
        issues = test_mcp_configuration(name, mcp_config)

        if issues == ['OK']:
            print(f"  OK {name}: Working")
            working_mcps += 1
        else:
            print(f"  FAIL {name}: ISSUES FOUND")
            for issue in issues:
                print(f"    - {issue}")
            failed_mcps += 1
        print()

    # Summary
    print("=" * 70)
    print(" DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print(f"Working MCPs: {working_mcps}/{total_mcps}")
    print(f"Failed MCPs: {failed_mcps}/{total_mcps}")

    if failed_mcps > 0:
        print(f"\nRECOMMENDED FIXES:")
        print("1. Update FEDERATED-INSTALLER-UNIFIED.py with correct package names")
        print("2. Fix GitHub repository URLs or use existing working paths")
        print("3. Change all 'python' commands to 'python3'")
        print("4. Add duplicate prevention logic")
    else:
        print(f"\nAll MCPs are properly configured!")

    return 1 if failed_mcps > 0 else 0

if __name__ == "__main__":
    sys.exit(main())