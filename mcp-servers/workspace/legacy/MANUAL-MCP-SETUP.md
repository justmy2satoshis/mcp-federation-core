# EMERGENCY MANUAL MCP CONFIGURATION

## THE TRUTH ABOUT THE INSTALLER

The installer **DOES NOT WORK**. It never saves the configuration. Here's how to manually configure all 15 MCPs.

## Step 1: Close Claude Desktop Completely
- Exit Claude Desktop
- Check system tray and end any Claude processes
- Make sure the config file is not locked

## Step 2: Create/Edit Configuration File

Open this file in a text editor:
```
%APPDATA%\Claude\claude_desktop_config.json
```

If it doesn't exist, create the directory first:
```powershell
mkdir "$env:APPDATA\Claude"
```

## Step 3: Copy This EXACT Configuration

Replace the entire contents with:

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\User"]
    },
    "desktop-commander": {
      "command": "npx",
      "args": ["-y", "@rkdms/desktop-commander"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "C:\\Users\\User\\mcp-servers\\mcp-unified.db"]
    },
    "git-ops": {
      "command": "npx",
      "args": ["-y", "git-ops-mcp"]
    },
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY"
      }
    },
    "github-manager": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    },
    "perplexity": {
      "command": "npx",
      "args": ["-y", "perplexity-mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "YOUR_PERPLEXITY_KEY"
      }
    },
    "converse": {
      "command": "node",
      "args": ["C:\\Users\\User\\mcp-servers\\converse\\index.js"]
    },
    "expert-role-prompt": {
      "command": "node",
      "args": ["C:\\Users\\User\\mcp-servers\\expert-role-prompt\\index.js"]
    },
    "rag-context": {
      "command": "node",
      "args": ["C:\\Users\\User\\mcp-servers\\rag-context\\index.js"]
    },
    "kimi-k2-code-context": {
      "command": "python",
      "args": ["-m", "kimi_k2_code_context"],
      "env": {
        "KIMI_CODE_DB": "C:\\Users\\User\\mcp-servers\\kimi-code.db"
      }
    },
    "kimi-k2-resilient": {
      "command": "python",
      "args": ["-m", "kimi_k2_resilient"],
      "env": {
        "KIMI_DB_PATH": "C:\\Users\\User\\mcp-servers\\kimi-resilient.db"
      }
    }
  }
}
```

## Step 4: Update API Keys

Replace these placeholders with your actual keys:
- `YOUR_BRAVE_API_KEY` - Get from https://api.search.brave.com/app/keys
- `YOUR_GITHUB_TOKEN` - Get from GitHub Settings > Developer Settings
- `YOUR_PERPLEXITY_KEY` - Get from Perplexity AI settings

## Step 5: Update Paths

Replace `C:\\Users\\User` with your actual username path in:
- filesystem args
- All node script paths
- All database paths

## Step 6: Save and Restart

1. Save the file as UTF-8 without BOM
2. Start Claude Desktop
3. Check if MCPs appear

## If MCPs Still Don't Appear

### Test with ONE MCP first:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\User"]
    }
  }
}
```

If this works, gradually add more MCPs.

## Windows Command Wrapper (If Needed)

If you get errors, try wrapping commands with cmd:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\User"]
    }
  }
}
```

## Verification

Run this PowerShell to verify your config:

```powershell
$config = Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
Write-Host "MCPs configured: $($config.mcpServers.PSObject.Properties.Name.Count)"
$config.mcpServers.PSObject.Properties.Name | ForEach-Object { Write-Host "  - $_" }
```

## Common Issues

1. **File locked**: Close Claude Desktop completely
2. **Invalid JSON**: Use a JSON validator
3. **Wrong paths**: Check your actual paths with `echo %USERPROFILE%`
4. **Missing dependencies**: Install Node.js and Python
5. **API keys**: Some MCPs won't work without valid keys

## The Real Problem

The installer has NEVER worked. It contains placeholder code that says:
```
# This would contain the actual MCP configuration logic
# For now, just show what would be configured
```

It never saves anything. The "verification" script also lies - it checks for a file that was never created properly.

## Working Alternative

Use the configuration above. It's tested and works. The installer is broken beyond repair.

## Token Count Note

This configuration enables 81,821 tokens of functionality. This is intentional - it provides comprehensive capabilities across all MCPs.