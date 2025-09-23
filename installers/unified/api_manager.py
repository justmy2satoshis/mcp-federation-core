#!/usr/bin/env python3
"""
API Key Manager for MCP Federation Core
Interactive configuration and validation of API keys
"""

import os
import json
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import getpass

class APIKeyManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.env_file = repo_root / '.env'
        self.logger = logging.getLogger(__name__)

        # API service configurations
        self.api_services = {
            'MOONSHOT_API_KEY': {
                'name': 'Kimi K2 (Moonshot)',
                'description': 'For Kimi K2 enhanced context and resilient processing',
                'url': 'https://platform.moonshot.cn/',
                'test_endpoint': 'https://api.moonshot.cn/v1/models',
                'required': True,
                'example': 'mk-...'
            },
            'PERPLEXITY_API_KEY': {
                'name': 'Perplexity',
                'description': 'For enhanced web search and Q&A capabilities',
                'url': 'https://perplexity.ai/settings/api',
                'test_endpoint': 'https://api.perplexity.ai/chat/completions',
                'required': True,
                'example': 'pplx-...'
            },
            'OPENAI_API_KEY': {
                'name': 'OpenAI',
                'description': 'For GPT models fallback (when Ollama unavailable)',
                'url': 'https://platform.openai.com/api-keys',
                'test_endpoint': 'https://api.openai.com/v1/models',
                'required': False,
                'example': 'sk-...'
            },
            'BRAVE_API_KEY': {
                'name': 'Brave Search',
                'description': 'For web search capabilities',
                'url': 'https://api.search.brave.com/app/keys',
                'test_endpoint': 'https://api.search.brave.com/res/v1/web/search',
                'required': False,
                'example': 'BSA...'
            },
            'XAI_API_KEY': {
                'name': 'xAI (Grok)',
                'description': 'For Grok model access',
                'url': 'https://console.x.ai/',
                'test_endpoint': 'https://api.x.ai/v1/models',
                'required': False,
                'example': 'xai-...'
            },
            'ANTHROPIC_API_KEY': {
                'name': 'Anthropic (Claude)',
                'description': 'For Claude models fallback',
                'url': 'https://console.anthropic.com/',
                'test_endpoint': 'https://api.anthropic.com/v1/models',
                'required': False,
                'example': 'sk-ant-...'
            },
            'COHERE_API_KEY': {
                'name': 'Cohere',
                'description': 'For embeddings and text processing',
                'url': 'https://dashboard.cohere.ai/api-keys',
                'test_endpoint': 'https://api.cohere.ai/v1/models',
                'required': False,
                'example': 'co-...'
            },
            'OPENROUTER_API_KEY': {
                'name': 'OpenRouter',
                'description': 'For multi-provider model access',
                'url': 'https://openrouter.ai/keys',
                'test_endpoint': 'https://openrouter.ai/api/v1/models',
                'required': False,
                'example': 'sk-or-...'
            },
            'GITHUB_PERSONAL_ACCESS_TOKEN': {
                'name': 'GitHub',
                'description': 'For GitHub repository management',
                'url': 'https://github.com/settings/personal-access-tokens',
                'test_endpoint': 'https://api.github.com/user',
                'required': False,
                'example': 'ghp_...'
            }
        }

    def load_existing_keys(self) -> Dict[str, str]:
        """Load existing API keys from .env file"""
        existing = {}

        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        existing[key.strip()] = value.strip().strip('"\'')

        return existing

    def interactive_setup(self) -> Dict[str, str]:
        """Interactive API key setup wizard"""
        print("\n" + "="*70)
        print("API KEY CONFIGURATION WIZARD")
        print("="*70)
        print("\nThis wizard will help you configure API keys for various services.")
        print("Required services are marked with [REQUIRED]")
        print("Optional services can be skipped by pressing Enter")
        print("\nYou can always add keys later by editing the .env file")

        existing_keys = self.load_existing_keys()
        configured_keys = existing_keys.copy()

        for env_var, config in self.api_services.items():
            print(f"\n{'-'*50}")
            print(f"Service: {config['name']}")
            print(f"Purpose: {config['description']}")
            print(f"Get key: {config['url']}")

            required_text = "[REQUIRED]" if config['required'] else "[OPTIONAL]"
            print(f"Status: {required_text}")

            # Check if key already exists
            if env_var in existing_keys:
                print(f"✓ Already configured: {existing_keys[env_var][:10]}...")
                choice = input("Keep existing key? (Y/n): ").strip().lower()
                if choice in ['', 'y', 'yes']:
                    continue

            # Get new key
            while True:
                if config['required']:
                    prompt = f"Enter {config['name']} API key (required): "
                else:
                    prompt = f"Enter {config['name']} API key (or press Enter to skip): "

                try:
                    key = getpass.getpass(prompt).strip()
                except KeyboardInterrupt:
                    print("\nSetup cancelled by user")
                    return {}

                if not key:
                    if config['required']:
                        print("❌ This key is required. Please enter a valid key.")
                        continue
                    else:
                        print("⏭️ Skipped")
                        break

                # Basic validation
                if not key.startswith(config['example'].split('-')[0]):
                    print(f"⚠️ Warning: Key doesn't match expected format ({config['example']})")
                    choice = input("Use this key anyway? (y/N): ").strip().lower()
                    if choice not in ['y', 'yes']:
                        continue

                # Test the key
                print(f"🔍 Testing {config['name']} API key...")
                if self.test_api_key(env_var, key):
                    print(f"✅ {config['name']} key is valid!")
                    configured_keys[env_var] = key
                    break
                else:
                    print(f"❌ {config['name']} key failed validation")
                    choice = input("Try a different key? (Y/n): ").strip().lower()
                    if choice in ['n', 'no']:
                        if not config['required']:
                            break
                        else:
                            print("This key is required for proper functionality.")

        return configured_keys

    def test_api_key(self, env_var: str, key: str) -> bool:
        """Test if an API key is valid"""
        config = self.api_services.get(env_var)
        if not config or not config.get('test_endpoint'):
            return True  # Skip test if no endpoint configured

        try:
            headers = self._get_auth_headers(env_var, key)
            response = requests.get(
                config['test_endpoint'],
                headers=headers,
                timeout=10
            )

            # Different APIs return different success codes
            if env_var == 'BRAVE_API_KEY':
                # Brave returns 400 without query, but with valid auth header
                return response.status_code in [200, 400]
            elif env_var == 'GITHUB_PERSONAL_ACCESS_TOKEN':
                return response.status_code == 200
            else:
                return response.status_code in [200, 401]  # 401 means auth header was processed

        except Exception as e:
            self.logger.debug(f"API test error for {env_var}: {e}")
            return False

    def _get_auth_headers(self, env_var: str, key: str) -> Dict[str, str]:
        """Get appropriate auth headers for different APIs"""
        if env_var in ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'XAI_API_KEY']:
            return {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
        elif env_var == 'BRAVE_API_KEY':
            return {
                'X-Subscription-Token': key,
                'Accept': 'application/json'
            }
        elif env_var == 'GITHUB_PERSONAL_ACCESS_TOKEN':
            return {
                'Authorization': f'token {key}',
                'Accept': 'application/vnd.github.v3+json'
            }
        elif env_var == 'COHERE_API_KEY':
            return {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
        elif env_var == 'MOONSHOT_API_KEY':
            return {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
        elif env_var == 'PERPLEXITY_API_KEY':
            return {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
        else:
            return {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }

    def save_keys(self, keys: Dict[str, str]) -> bool:
        """Save API keys to .env file"""
        try:
            # Create backup if file exists
            if self.env_file.exists():
                backup_file = self.env_file.with_suffix('.env.backup')
                self.env_file.rename(backup_file)
                self.logger.info(f"Backed up existing .env to {backup_file}")

            # Write new .env file
            with open(self.env_file, 'w') as f:
                f.write("# MCP Federation Core - API Keys\n")
                f.write(f"# Generated on {os.popen('date').read().strip()}\n")
                f.write("# Keep this file secure and do not commit to version control\n\n")

                for env_var, key in keys.items():
                    if key:  # Only write non-empty keys
                        config = self.api_services.get(env_var, {})
                        service_name = config.get('name', env_var)
                        f.write(f"# {service_name}\n")
                        f.write(f"{env_var}={key}\n\n")

            self.logger.info(f"✓ API keys saved to {self.env_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save API keys: {e}")
            return False

    def validate_all_keys(self) -> Dict[str, bool]:
        """Validate all configured API keys"""
        existing_keys = self.load_existing_keys()
        results = {}

        print("\n🔍 Validating API keys...")

        for env_var, key in existing_keys.items():
            if env_var in self.api_services:
                config = self.api_services[env_var]
                print(f"  Testing {config['name']}...", end=' ')

                if self.test_api_key(env_var, key):
                    print("✅ Valid")
                    results[env_var] = True
                else:
                    print("❌ Invalid")
                    results[env_var] = False

        return results

    def setup_api_keys(self, interactive: bool = True) -> bool:
        """Main API key setup process"""
        if interactive:
            keys = self.interactive_setup()
            if keys:
                return self.save_keys(keys)
            else:
                self.logger.info("API key setup cancelled")
                return False
        else:
            # Non-interactive mode - validate existing keys
            existing = self.load_existing_keys()
            if existing:
                self.logger.info("Validating existing API keys...")
                results = self.validate_all_keys()
                valid_count = sum(results.values())
                total_count = len(results)
                self.logger.info(f"✓ {valid_count}/{total_count} API keys valid")
                return valid_count > 0
            else:
                self.logger.warning("No API keys found. Run with --setup-keys for interactive setup")
                return False

if __name__ == '__main__':
    # Test API key manager
    from pathlib import Path

    repo_root = Path('.')
    api_manager = APIKeyManager(repo_root)

    print("Testing API Key Manager...")
    if api_manager.setup_api_keys(interactive=False):
        print("✓ API key validation passed")
    else:
        print("✗ No valid API keys found")