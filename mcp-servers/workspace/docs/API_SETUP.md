# API Keys Setup Guide

## Overview

MCP Federation Core integrates with multiple AI providers and services. Some MCPs require API keys to function, while others work out-of-the-box.

## Required API Keys

These keys are essential for core functionality:

### 1. Brave Search API
**Required for**: Web Search MCP
**Free Tier**: Yes (2,000 queries/month)
**Get Key**: https://api.search.brave.com/app/keys

```bash
# Add to .env file:
BRAVE_SEARCH_API_KEY=your_brave_api_key_here
```

### 2. Perplexity API
**Required for**: Perplexity MCP
**Free Tier**: Limited
**Get Key**: https://www.perplexity.ai/settings/api

```bash
# Add to .env file:
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

## Optional API Keys

These enhance functionality but aren't required:

### OpenAI
**Used by**: Converse MCP (GPT models)
**Get Key**: https://platform.openai.com/api-keys

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Moonshot AI (Kimi)
**Used by**: Kimi K2 MCPs
**Get Key**: https://platform.moonshot.cn/console/api-keys

```bash
MOONSHOT_API_KEY=your_moonshot_api_key_here
```

### xAI (Grok)
**Used by**: Converse MCP (Grok models)
**Get Key**: https://console.x.ai/

```bash
XAI_API_KEY=your_xai_api_key_here
```

### Cohere
**Used by**: Converse MCP (Command models)
**Get Key**: https://dashboard.cohere.com/api-keys

```bash
COHERE_API_KEY=your_cohere_api_key_here
```

### OpenRouter
**Used by**: Converse MCP (model routing)
**Get Key**: https://openrouter.ai/keys

```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### GitHub Personal Access Token
**Used by**: GitHub Manager MCP
**Get Token**: https://github.com/settings/tokens

```bash
GITHUB_TOKEN=your_github_pat_here
```

## Setup Methods

### Method 1: During Installation (Recommended)

The installer automatically prompts for API keys:

```powershell
# Windows
irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-safe.ps1 | iex

# When prompted, enter your keys
```

### Method 2: Manual Configuration

Edit the `.env` file directly:

```bash
# Windows
notepad %USERPROFILE%\mcp-servers\.env

# macOS/Linux
nano ~/mcp-servers/.env
```

### Method 3: Environment Variables

Set system environment variables:

```powershell
# Windows (PowerShell as Admin)
[System.Environment]::SetEnvironmentVariable("BRAVE_SEARCH_API_KEY", "your_key", "User")

# macOS/Linux
export BRAVE_SEARCH_API_KEY="your_key"
echo 'export BRAVE_SEARCH_API_KEY="your_key"' >> ~/.bashrc
```

## Validation

Check if your API keys are working:

```bash
# Run validation script
python ~/mcp-servers/installers/unified/validator.py

# Or test individual MCPs in Claude Desktop
# Type: @web-search test query
# Type: @perplexity what is MCP?
```

## Security Best Practices

### DO:
- Store keys in `.env` file (gitignored)
- Use environment variables for production
- Rotate keys regularly
- Use separate keys for dev/prod

### DON'T:
- Commit keys to git repositories
- Share keys in public forums
- Use production keys for testing
- Store keys in code files

## Free Alternatives

### Ollama (Local AI)
Converse MCP automatically detects Ollama:

```bash
# Install Ollama
# Windows: Download from https://ollama.ai
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama
ollama pull mistral
```

With Ollama installed, Converse MCP uses local models by default, saving API costs!

## Troubleshooting API Keys

### "Invalid API Key" Error
- Check for extra spaces or quotes
- Verify key is active on provider dashboard
- Ensure .env file is in correct location

### "Rate Limit Exceeded"
- Check your plan limits
- Implement caching if possible
- Consider upgrading plan

### Keys Not Loading
- Restart Claude Desktop after adding keys
- Check .env file permissions
- Verify path: `~/mcp-servers/.env`

### Testing Individual Keys

```python
# Test script: ~/mcp-servers/test_api_keys.py
import os
from dotenv import load_dotenv

load_dotenv()

keys_to_check = [
    "BRAVE_SEARCH_API_KEY",
    "PERPLEXITY_API_KEY",
    "OPENAI_API_KEY",
    "GITHUB_TOKEN"
]

for key_name in keys_to_check:
    key_value = os.getenv(key_name)
    if key_value:
        print(f"[OK] {key_name}: {'*' * 8}{key_value[-4:]}")
    else:
        print(f"[MISSING] {key_name}")
```

## Cost Optimization

### Free Tier Usage
- **Brave Search**: 2,000 queries/month free
- **GitHub**: Unlimited public repo access
- **Ollama**: Completely free (local)

### Cost-Saving Tips
1. Use Ollama for development/testing
2. Cache API responses when possible
3. Batch requests to reduce calls
4. Monitor usage via provider dashboards

### Estimated Monthly Costs
With typical usage (1000 queries/day):
- **With Ollama**: ~$5-10/month
- **Without Ollama**: ~$30-50/month
- **Savings**: 80-95%

## API Key Requirements by MCP

| MCP | Required Keys | Optional Keys | Works Without Keys |
|-----|--------------|---------------|-------------------|
| sqlite | None | None | Yes |
| filesystem | None | None | Yes |
| memory | None | None | Yes |
| sequential-thinking | None | None | Yes |
| desktop-commander | None | None | Yes |
| playwright | None | None | Yes |
| git-ops | None | GitHub Token | Yes (limited) |
| expert-role-prompt | None | None | Yes |
| rag-context | None | None | Yes |
| kimi-k2-resilient | None | Moonshot | Yes (limited) |
| kimi-k2-code-context | None | Moonshot | Yes (limited) |
| web-search | Brave API | None | No |
| perplexity | Perplexity API | None | No |
| github-manager | GitHub Token | None | No |
| converse | None | Multiple | Yes (with Ollama) |

## Quick Start Checklist

- [ ] Get Brave Search API key (free)
- [ ] Get Perplexity API key
- [ ] Install Ollama (optional, saves money)
- [ ] Add keys to .env file
- [ ] Restart Claude Desktop
- [ ] Run validator to confirm

## Support

Having issues with API keys?

1. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
2. Run validator: `python ~/mcp-servers/installers/unified/validator.py`
3. Create issue: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)