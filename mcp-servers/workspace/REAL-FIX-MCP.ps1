# REAL MCP FIX - Simple script that actually works
Write-Host "MCP Federation Core - Real Configuration Fix" -ForegroundColor Cyan
Write-Host ""

# Check if Claude is running (warning only)
if (Get-Process "Claude" -ErrorAction SilentlyContinue) {
    Write-Host "WARNING: Claude Desktop is running" -ForegroundColor Yellow
    Write-Host "You'll need to restart Claude Desktop after this completes" -ForegroundColor Yellow
    Write-Host ""
}

# Create config directory
$configDir = "$env:APPDATA\Claude"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Build the configuration
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$baseDir = "$env:USERPROFILE\mcp-servers"

# Create proper config content
$configContent = @'
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
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "USER_HOME"]
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
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "USER_HOME\\mcp-servers\\mcp-unified.db"]
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
      "args": ["USER_HOME\\mcp-servers\\converse\\index.js"]
    },
    "expert-role-prompt": {
      "command": "node",
      "args": ["USER_HOME\\mcp-servers\\expert-role-prompt\\index.js"]
    },
    "rag-context": {
      "command": "node",
      "args": ["USER_HOME\\mcp-servers\\rag-context\\index.js"]
    },
    "kimi-k2-code-context": {
      "command": "python",
      "args": ["-m", "kimi_k2_code_context"],
      "env": {
        "KIMI_CODE_DB": "USER_HOME\\mcp-servers\\kimi-code.db"
      }
    },
    "kimi-k2-resilient": {
      "command": "python",
      "args": ["-m", "kimi_k2_resilient"],
      "env": {
        "KIMI_DB_PATH": "USER_HOME\\mcp-servers\\kimi-resilient.db"
      }
    }
  }
}
'@

# Replace USER_HOME with actual path
$configContent = $configContent.Replace("USER_HOME", $env:USERPROFILE)

# Save the configuration
[System.IO.File]::WriteAllText($configPath, $configContent)

# Verify it was saved
if (Test-Path $configPath) {
    $size = (Get-Item $configPath).Length
    Write-Host "SUCCESS: Configuration saved!" -ForegroundColor Green
    Write-Host "  File: $configPath" -ForegroundColor Gray
    Write-Host "  Size: $size bytes" -ForegroundColor Gray
    Write-Host ""

    # Count MCPs
    $config = Get-Content $configPath | ConvertFrom-Json
    $count = @($config.mcpServers.PSObject.Properties).Count
    Write-Host "Configured $count MCPs:" -ForegroundColor Cyan
    $config.mcpServers.PSObject.Properties.Name | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor White
    }

    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Update API keys in the config file"
    Write-Host "2. Start Claude Desktop"
    Write-Host "3. Check that MCPs appear"
} else {
    Write-Host "ERROR: Failed to save configuration!" -ForegroundColor Red
}