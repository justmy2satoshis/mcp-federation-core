#!/usr/bin/env python3
"""
MCP Federation Core v0.1.4 - MCP Verification Diagnostic Tool
Tests each MCP to ensure they show green checkmarks in Claude Desktop
"""

import json
import subprocess
import os
from pathlib import Path
import platform
import sys
import time

class MCPVerifier:
    def __init__(self):
        self.home = Path.home()
        self.config_path = self._get_config_path()
        self.results = {}
        self.platform = platform.system()

    def _get_config_path(self):
        """Get the correct Claude Desktop config path for the OS"""
        if platform.system() == "Windows":
            return Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json"
        elif platform.system() == "Darwin":  # macOS
            return self.home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return self.home / ".config" / "Claude" / "claude_desktop_config.json"

    def load_config(self):
        """Load Claude Desktop configuration"""
        if not self.config_path.exists():
            print(f"[ERROR] Configuration not found at: {self.config_path}")
            return None

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Error loading config: {e}")
            return None

    def test_mcp_command(self, name, config):
        """Test if an MCP command executes successfully"""
        command = config.get('command', '')
        args = config.get('args', [])

        # Build full command
        if command == 'npx':
            # Test npx availability
            test_cmd = ['npx', '--version']
        elif command == 'node':
            # For node commands, test with --version on the script
            if args and args[0].endswith('.js'):
                # Can't test arbitrary scripts, check if file exists
                script_path = Path(args[0])
                if script_path.exists():
                    return {'status': 'exists', 'message': f"Script found: {args[0]}"}
                else:
                    return {'status': 'missing', 'message': f"Script not found: {args[0]}"}
            else:
                test_cmd = ['node', '--version']
        elif command in ['python', 'python3']:
            # For Python scripts, check if file exists
            if args and args[0].endswith('.py'):
                script_path = Path(args[0])
                if script_path.exists():
                    return {'status': 'exists', 'message': f"Python script found: {args[0]}"}
                else:
                    return {'status': 'missing', 'message': f"Python script not found: {args[0]}"}
            else:
                test_cmd = [command, '--version']
        else:
            # Unknown command type
            return {'status': 'unknown', 'message': f"Unknown command type: {command}"}

        # Execute test command
        try:
            result = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                timeout=5,
                shell=(self.platform == "Windows")
            )

            if result.returncode == 0:
                # Now test the actual MCP if it's npx
                if command == 'npx' and args:
                    # Test if the package exists
                    package = args[-1] if args else ''
                    test_package_cmd = ['npm', 'view', package, 'version']

                    try:
                        pkg_result = subprocess.run(
                            test_package_cmd,
                            capture_output=True,
                            text=True,
                            timeout=10,
                            shell=(self.platform == "Windows")
                        )

                        if pkg_result.returncode == 0:
                            version = pkg_result.stdout.strip()
                            return {'status': 'ok', 'message': f"Package found (v{version})"}
                        else:
                            return {'status': 'missing', 'message': f"Package not found: {package}"}
                    except Exception as e:
                        return {'status': 'error', 'message': f"Error checking package: {e}"}

                return {'status': 'ok', 'message': 'Command available'}
            else:
                return {'status': 'error', 'message': f"Command failed: {result.stderr}"}

        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'message': 'Command timed out'}
        except FileNotFoundError:
            return {'status': 'missing', 'message': f"Command not found: {command}"}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def verify_all_mcps(self):
        """Verify all MCPs in the configuration"""
        print("\n" + "="*70)
        print(" MCP FEDERATION CORE v0.1.4 - MCP VERIFICATION DIAGNOSTIC")
        print("="*70)

        config = self.load_config()
        if not config:
            return False

        mcpServers = config.get('mcpServers', {})

        if not mcpServers:
            print("[WARNING] No MCPs configured")
            return False

        print(f"\n[STATS] Found {len(mcpServers)} MCPs to verify\n")

        # Track statistics
        stats = {
            'ok': 0,
            'missing': 0,
            'error': 0,
            'unknown': 0,
            'exists': 0,
            'timeout': 0
        }

        # Test each MCP
        for i, (name, mcp_config) in enumerate(mcpServers.items(), 1):
            print(f"[{i}/{len(mcpServers)}] Testing {name}...")

            result = self.test_mcp_command(name, mcp_config)
            self.results[name] = result

            # Update stats
            stats[result['status']] = stats.get(result['status'], 0) + 1

            # Display result with appropriate symbol
            if result['status'] == 'ok':
                symbol = "[OK]"
            elif result['status'] == 'exists':
                symbol = "[EXISTS]"
            elif result['status'] == 'missing':
                symbol = "[MISSING]"
            elif result['status'] == 'error':
                symbol = "[ERROR]"
            elif result['status'] == 'timeout':
                symbol = "[TIMEOUT]"
            else:
                symbol = "[UNKNOWN]"

            print(f"    {symbol} {name}: {result['message']}")

        # Display summary
        print("\n" + "="*70)
        print(" VERIFICATION SUMMARY")
        print("="*70)

        print(f"\n[RESULTS]:")
        print(f"  [OK] Working MCPs: {stats['ok']}")
        print(f"  [EXISTS] Scripts exist: {stats['exists']}")
        print(f"  [MISSING] Missing packages: {stats['missing']}")
        print(f"  [ERROR] Errors: {stats['error']}")
        print(f"  [TIMEOUT] Timeouts: {stats['timeout']}")
        print(f"  [UNKNOWN] Unknown: {stats['unknown']}")

        # List problematic MCPs
        problems = []
        for name, result in self.results.items():
            if result['status'] not in ['ok', 'exists']:
                problems.append((name, result))

        if problems:
            print(f"\n[WARNING] PROBLEMATIC MCPs ({len(problems)}):")
            for name, result in problems:
                print(f"\n  {name}:")
                print(f"    Status: {result['status']}")
                print(f"    Issue: {result['message']}")

                # Provide fix suggestions
                if 'not found' in result['message'].lower():
                    if 'server-' in result['message']:
                        print(f"    Fix: npm install -g {result['message'].split(':')[-1].strip()}")
                    elif '.py' in result['message']:
                        print(f"    Fix: Check Python script path in configuration")
                elif 'timeout' in result['message'].lower():
                    print(f"    Fix: MCP may be slow to start - check logs")
        else:
            print("\n[SUCCESS] ALL MCPs VERIFIED SUCCESSFULLY!")
            print("   All MCPs should show green checkmarks in Claude Desktop")

        # Save detailed results
        results_file = Path("mcp_verification_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'platform': self.platform,
                'config_path': str(self.config_path),
                'total_mcps': len(mcpServers),
                'statistics': stats,
                'results': self.results
            }, f, indent=2)

        print(f"\n[SAVED] Detailed results saved to: {results_file}")

        # Return True if all MCPs are ok or exist
        return all(r['status'] in ['ok', 'exists'] for r in self.results.values())

    def fix_common_issues(self):
        """Suggest fixes for common MCP issues"""
        print("\n" + "="*70)
        print(" COMMON FIX SUGGESTIONS")
        print("="*70)

        print("\n[FIX] If MCPs show warning triangles in Claude Desktop:")
        print("\n1. Missing npm packages:")
        print("   npm install -g @modelcontextprotocol/server-memory")
        print("   npm install -g @modelcontextprotocol/server-filesystem")
        print("   npm install -g @modelcontextprotocol/server-sqlite")
        print("   npm install -g server-perplexity-ask")
        print("   npm install -g converse-mcp-server")

        print("\n2. Python command issues (Windows):")
        print("   Change 'python3' to 'python' in configuration")

        print("\n3. Missing API keys:")
        print("   Add required environment variables to MCP configs:")
        print("   - GITHUB_PERSONAL_ACCESS_TOKEN")
        print("   - BRAVE_API_KEY")
        print("   - PERPLEXITY_API_KEY")

        print("\n4. Path issues:")
        print("   Ensure all Python script paths are absolute")
        print("   Check that cloned GitHub repos exist in expected locations")

        print("\n5. After fixing:")
        print("   - Save configuration file")
        print("   - Completely restart Claude Desktop")
        print("   - Run this verification tool again")

def main():
    verifier = MCPVerifier()

    # Run verification
    success = verifier.verify_all_mcps()

    # Show fix suggestions if there were problems
    if not success:
        verifier.fix_common_issues()

    print("\n" + "="*70)
    print(" VERIFICATION COMPLETE")
    print("="*70)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()